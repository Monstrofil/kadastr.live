import logging
import os
from argparse import ArgumentParser
import geojson
from django.contrib.gis.geos import GEOSGeometry
from django.db.transaction import atomic

from geojson.feature import FeatureCollection

from django.core.management.base import BaseCommand
from tqdm import tqdm

from geodata.models import GeoJsonUpload, GeoRecord


@atomic
def update_database(filepath: str):
    if not os.path.exists(filepath):
        print('File %s not found.' % os.path.abspath(filepath))
        exit(1)

    with open(filepath) as f:
        collection = geojson.load(f)

    upload = GeoJsonUpload.objects.create(
        content_hash='test',
        filename=os.path.basename(filepath),
    )

    if not isinstance(collection, FeatureCollection):
        print('GeoJson does not have FeatureCollection as root.')
        exit(1)

    records = []
    for feature in tqdm(collection.features):
        if not feature.geometry:
            logging.warning('Feature has no valid geometry, skip')
            continue

        record = GeoRecord(
            group=os.path.basename(filepath),
            geometry_zoom_8=GEOSGeometry(str(feature.geometry), srid=4326).simplify(
                tolerance=0.01),
            geometry_zoom_10=GEOSGeometry(str(feature.geometry), srid=4326).simplify(
                tolerance=0.0005),
            geometry_zoom_12=GEOSGeometry(str(feature.geometry), srid=4326).simplify(
                tolerance=0.0000038),
            geometry=GEOSGeometry(str(feature.geometry), srid=4326),
            properties=dict(feature.properties),
            revision=upload,
        )
        records.append(record)

    GeoRecord.objects.bulk_create(records, batch_size=1000)



class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser: ArgumentParser):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(processName)s %(threadName)s %(message)s')

        subparsers = parser.add_subparsers(dest='action', required=True)

        update = subparsers.add_parser('update', help='Updates list of parcels from official api')

        update.add_argument('--path', help='Path to the file for the import', required=True)

    def handle(self, action, path, *args, **kwargs):
        logging.basicConfig(level=logging.INFO)

        if action == 'update':
            update_database(os.path.dirname(__file__) + '/' + path)
