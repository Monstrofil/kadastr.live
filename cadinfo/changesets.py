import logging

from django.db import transaction

from cadinfo.models import Update, LanduseChange, Landuse


def create_changeset(revision: Update, previous: Update):
    change = LanduseChange.objects.filter(revision=revision, previous=previous).first()
    if change is not None:
        return None

    with transaction.atomic():

        added_parcels = Landuse.objects.filter(
            revision=revision.id
        ).exclude(
            cadnum__in=(
                Landuse.objects.filter(
                    revision=previous.id
                ).values_list('cadnum', flat=True)
            )
        ).values_list('cadnum', flat=True)

        logging.info('Adding %s added parcels', len(list(added_parcels)))

        LanduseChange.objects.bulk_create([
            LanduseChange(
                revision=revision,
                previous=previous,
                cadnum=cadnum,
                action=LanduseChange.Action.CREATE
            ) for cadnum in added_parcels
        ], batch_size=1000)

        removed_parcels = Landuse.objects.filter(
            revision=previous.id
        ).exclude(
            cadnum__in=(
                Landuse.objects.filter(
                    revision=revision.id
                ).values_list('cadnum', flat=True)
            )
        ).values_list('cadnum', flat=True)

        logging.info('Adding %s removed parcels', len(list(removed_parcels)))

        LanduseChange.objects.bulk_create([
            LanduseChange(
                revision=revision,
                previous=previous,
                cadnum=cadnum,
                action=LanduseChange.Action.DELETE
            ) for cadnum in removed_parcels
        ], batch_size=1000)

        changed_parcels = Landuse.objects.raw("""
            SELECT A.id, A.cadnum
            FROM landuse A
               INNER JOIN landuse B on A.revision = %s AND B.revision = %s AND A.cadnum = B.cadnum
            WHERE 
            NOT EXISTS(
               SELECT A.cadnum, A.category, A.purpose_code, A.purpose, A.use, 
                      A.area, A.unit_area, A.ownershipcode, 
                      A.geometry
               INTERSECT
               SELECT B.cadnum, B.category, B.purpose_code, B.purpose, B.use, 
                      B.area, B.unit_area, B.ownershipcode, 
                      B.geometry)
        
        """, params=(revision.id, previous.id))

        logging.info('Adding %s changed parcels', len(list(changed_parcels)))

        LanduseChange.objects.bulk_create([
            LanduseChange(
                revision=revision,
                previous=previous,
                cadnum=landuse.cadnum,
                action=LanduseChange.Action.UPDATE
            ) for landuse in changed_parcels
        ], batch_size=1000)
