import glob
import json
import queue
import threading
import time
from operator import itemgetter, attrgetter
from typing import Dict

import tqdm
from dataclasses import dataclass

import logging
import os
from functools import partial
from multiprocessing import current_process
from datetime import date, datetime

from django.db import connections, reset_queries
from django.db.models import Count
from multiprocessing_logging import install_mp_handler

import cachetools.func
import requests
from django.contrib.gis.geos import GEOSGeometry
from retry import retry
from tqdm.contrib.concurrent import process_map, thread_map
from tqdm.contrib.logging import logging_redirect_tqdm

from cadinfo.changesets import create_changeset
from cadinfo.models import Landuse, Update

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
KOATUU_PATHS = files = glob.glob(os.path.join(BASE_DIR, 'static', 'koatuu*.json'))

API_URL = 'https://e.land.gov.ua/api/parcel_info'
API_AUTH = 'OTgwXzIwOW1jeTEwOTUwazhnMDBnY29za2djd29' \
           'zczRjMHdrY3djOGc4czhvbzhjMHdnY2M4Omk2en' \
           'plY2hiaGVvazhrb2s4NHdnMGMwc2tnczAwd293Y' \
           'zg0a3N3Zzg0MGNvNG9zNGM='
API_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/90.0.4430.212 Safari/537.36'

today = date.today()


download_queue = queue.Queue()
process_queue = queue.Queue(maxsize=10)
download_complete = False


@dataclass
class Koatuu:
    name: str
    unique_id: str
    level: int
    parent: int
    pre_parent: int

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __hash__(self):
        return hash(self.unique_id)

@dataclass
class InsertTask:
    koatuu: Koatuu
    raw_parcels: Dict
    revision: Update


def download_koatuu(revision):
    while True:
        if download_queue.empty():
            logging.info('Downloading complete')
            break

        koatuu = download_queue.get()
        logging.info(f'Working on {koatuu}; %s items left' % download_queue.qsize())
        data = get_data(koatuu=koatuu)
        if data:
            process_queue.put(InsertTask(
                revision=revision,
                koatuu=koatuu,
                raw_parcels=data
            ))
        else:
            logging.warning('Skipping insert for %s', koatuu)
        logging.info(f'Finished {koatuu}')
        download_queue.task_done()


def insert_into_db():

    while True:
        try:
            task: InsertTask = process_queue.get(timeout=10)
        except queue.Empty as e:
            # everything is downloaded, no more pending tasks
            if download_complete:
                break
            logging.info('Download is not complete, but no pending tasks in queue')
            time.sleep(5)
            continue
        logging.info('Received task to insert parcels for %s; left=%s', task.koatuu.unique_id, process_queue.qsize())
        update_db(task)
        logging.info('Insert for %s succeeded', task.koatuu.unique_id)
        Update.objects.filter(
            id=task.revision.id
        ).update(
            latest_koatuu=task.koatuu.unique_id
        )

        reset_queries()
        del task


def _get_koatuu_data(filename):
    logging.info('Loading koatuu by path %s', filename)
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    logging.info('Koatuu loaded, records found %s', len(data))
    return data


@retry(max_retries=-1, interval=1, exceptions=(requests.RequestException, KeyError,))
def _refresh_token():
    r = requests.post(
        'https://e.land.gov.ua/oauth/v2/token',
        data=dict(grant_type='client_credentials'),
        headers={
            'Authorization': 'Basic %s' % API_AUTH,
            'User-Agent': API_USER_AGENT
        }
    )
    logging.info('Api response: %s', r.text)
    r.raise_for_status()
    return r.json()['access_token']


@cachetools.func.ttl_cache(maxsize=128, ttl=900)
def get_token():
    return _refresh_token()


def get_koatuu(info) -> Koatuu:
    r = [
        [info['Перший рівень'], info["Категорія"], info["Назва об'єкта українською мовою"], None, None],
        [info['Другий рівень'], info["Категорія"], info["Назва об'єкта українською мовою"], info['Перший рівень'], None],
        [info['Третій рівень'], info["Категорія"], info["Назва об'єкта українською мовою"], info['Другий рівень'], info['Перший рівень']],
        [info['Четвертий рівень'], info["Категорія"], info["Назва об'єкта українською мовою"], info['Третій рівень'], info['Другий рівень']],
    ]
    r.reverse()
    level, item = next((
        (level, item) for (level, item) in enumerate(r, start=0) if item[0]
    ))

    return Koatuu(
        name=item[2],
        unique_id=str(item[0]),
        parent=item[3],
        pre_parent=item[4],
        level=4 - level
    )


@retry(interval=5, max_retries=-1)
def get_data(koatuu: Koatuu):
    data, raw = _get_landuse_data(koatuu)

    if not data or 'error' in data:
        logging.warning('Unable to get data for koatuu %s', koatuu)
        logging.warning('Original information is %s', raw)
        return

    return data


def update_db(task: InsertTask):
    if not task.raw_parcels:
        return

    logging.info('Processing %s parcels in thread', len(task.raw_parcels))

    parcels_for_insert = []
    for parcel in tqdm.tqdm(task.raw_parcels):
        if parcel['ppoint']:
            if 'POINT' in parcel['ppoint']:
                point_geom = GEOSGeometry(parcel['ppoint'], srid=3857) if parcel['ppoint'] else None
            else:
                logging.error('Point %s is polygon for parcel %s', parcel['ppoint'], parcel['cadnum'])
                point_geom = None
        else:
            point_geom = None

        try:
            valuation_date = datetime.strptime(
                parcel['valuation_date'], '%Y-%m-%d %H:%M:%S'
            ).timestamp() if parcel['valuation_date'] else None
        except ValueError:
            # e.g. "valuation_date": "0001-01-01 00:00:00",
            # who knows why it happened
            valuation_date = None

        try:
            valuation_value = float(parcel['valuation_value']) if parcel['valuation_value'] else None
            if valuation_value and valuation_value > 10**14:
                # invalid values =/
                valuation_value = -1
        except ValueError:
            valuation_value = -1

        parcel = Landuse(
            cadnum=parcel['cadnum'],
            category=parcel['category'],
            purpose_code=parcel['purpose_code'],
            purpose=parcel['purpose'],
            use=parcel['use'],
            area=parcel['area'],
            unit_area=parcel['unit_area'],
            ownershipcode=parcel['ownershipcode'],
            ownership=parcel['ownership'],
            valuation_value=valuation_value,
            valuation_date=valuation_date,
            point=point_geom,
            bbox=GEOSGeometry(parcel['zoom_to'], srid=3857) if parcel['ppoint'] else None,
            koatuu=task.koatuu.unique_id if task.koatuu.level <= 2 else (
                task.koatuu.parent if task.koatuu.level == 3 else task.koatuu.pre_parent),
            geometry=GEOSGeometry(parcel['geom'], srid=4326) if parcel['geom'] else None,
            revision=task.revision
        )

        parcels_for_insert.append(parcel)

    logging.info('Inserting %s parcels in thread', len(task.raw_parcels))
    objs = Landuse.objects.bulk_create(parcels_for_insert, batch_size=500, ignore_conflicts=True)

    logging.info('Updating %s parcels complete', len(parcels_for_insert))

    del objs
    del parcels_for_insert


def _get_landuse_data(koatuu: Koatuu):
    logging.info('Downloading parcel data %s', koatuu)
    r = requests.post(
        API_URL,
        json=dict(
            cad_num=f'{koatuu.unique_id}:{0:02d}:{0:03d}:{0:04d}',
            request_owner="dzk"
        ),
        headers={
            'authorization': 'Bearer ' + get_token(),
            'User-Agent': API_USER_AGENT
        }, timeout=60 * 5
    )

    logging.info('Parcel downloaded %s', koatuu.unique_id)
    r.raise_for_status()
    data = r.json()
    return data, r.text


def _get_indexes():
    for filename in KOATUU_PATHS:
        for k in _get_koatuu_data(filename):
            koatuu = get_koatuu(k)
            logging.debug('Processing %s', koatuu)
            yield koatuu


def update_database():
    with logging_redirect_tqdm():
        install_mp_handler()

        latest_update = Update.get_latest_update(success=False)

        if latest_update.status not in [
            Update.Status.ERROR, Update.Status.SUCCESS
        ]:
            print('Last update revision=%s is still not ended (or hang or crashed). '
                  'Would you like to start new update (y) continue previous (N)?' % latest_update.id)
            response = input()
            if response.lower() == 'y':
                latest_update.status = 'error'
                latest_update.save()

                latest_update = Update.objects.create(
                    status=Update.Status.IN_PROGRESS
                )
        else:
            latest_update = Update.objects.create(
                status=Update.Status.IN_PROGRESS
            )

        # scraping level 3 indexes first
        level_3_koatuu = list(set([
            koatuu for koatuu in _get_indexes() if koatuu.level <= 2
        ]))
        # sort unique ids then (stable sort, so level is still sorted)
        level_3_koatuu.sort(key=attrgetter('unique_id'))
        # sort level from 1 to 3 keeping stable unique_id
        level_3_koatuu.sort(key=attrgetter('level'))

        if latest_update.latest_koatuu:
            logging.info("Searching for the latest koatuu scraped")
            latest_koatuu_obj = next(
                (koatuu for koatuu in level_3_koatuu if koatuu.unique_id == latest_update.latest_koatuu),
                None
            )
            if latest_koatuu_obj is None:
                level_3_koatuu = []
            else:
                logging.info("Found latest koatuu scraped %s", latest_koatuu_obj)
                level_3_koatuu = level_3_koatuu[level_3_koatuu.index(latest_koatuu_obj):]
                logging.info('Koatuu to scrape only %s', len(level_3_koatuu))

        if level_3_koatuu:
            _download_and_insert(latest_update, level_3_koatuu)
        logging.info('All insert l1 operations ended')
        # process level 4 indexes only for regions where parcels
        # number is more than 100000

        annotated = Landuse.objects.all().values(
            'koatuu'
        ).filter(
            revision=latest_update.id
        ).annotate(
            total=Count('koatuu')
        ).order_by('-total')

        level_4_koatuu = []
        all_koatuu = list(set([
            koatuu for koatuu in _get_indexes()
        ]))
        for result in annotated:
            if result['total'] < 100000:
                continue
            koatuu_obj = next(
                koatuu for koatuu in all_koatuu if koatuu.unique_id == str(result['koatuu']))

            if koatuu_obj.level == 2:
                level_3_koatuus = [
                    *set([
                        koatuu for koatuu in all_koatuu if
                        koatuu.level == 3 and str(koatuu.parent) == koatuu_obj.unique_id
                    ])
                ]
                level_4_koatuu.extend(level_3_koatuus)
                for level_3_koatuu in level_3_koatuus:
                    level_4_koatuu.extend([
                        *set([
                            koatuu for koatuu in all_koatuu if
                            koatuu.level == 4 and str(koatuu.parent) == level_3_koatuu.unique_id
                        ])
                    ])

            if koatuu_obj.level == 3:
                level_4_koatuu.extend([
                    *set([
                        koatuu for koatuu in all_koatuu if
                        koatuu.level == 4 and str(koatuu.parent) == koatuu_obj.unique_id
                    ])
                ])

        level_4_koatuu.sort(key=attrgetter('unique_id'))
        _download_and_insert(latest_update, level_4_koatuu)

    # detecting changes to create analysis table
    create_changeset(
        revision=Update.objects.get(id=latest_update.id),
        previous=Update.objects.get(id=Update.get_latest_update().id),
    )

    # everything is ok => success status
    Update.objects.filter(
        id=latest_update.id
    ).update(
        status=Update.Status.SUCCESS
    )


def _download_and_insert(latest_update, koatuu_list):
    logging.info('Total koatuu records %s', len(koatuu_list))
    global download_complete
    download_complete = False
    for koatuu in koatuu_list:
        download_queue.put(koatuu)

    # start multiple threads that will download parcels
    t1 = threading.Thread(target=partial(
        download_koatuu, revision=latest_update), daemon=True)
    t2 = threading.Thread(target=partial(
        download_koatuu, revision=latest_update), daemon=True)

    t1.start()
    t2.start()

    # and start multiple insert threads
    insert_threads = [
        threading.Thread(target=insert_into_db, daemon=True)
        for i in range(4)
    ]

    for thread in insert_threads:
        thread.start()

    # waiting for download threads to finish
    t1.join()
    t2.join()

    # marking download as complete
    download_complete = True

    while True:
        for thread in insert_threads:
            if thread.is_alive():
                time.sleep(5)
                break
        else:
            logging.info('All threads dead, qsize_download=%s, qsize_insert=%s',
                         download_queue.qsize(), process_queue.qsize())
            break




