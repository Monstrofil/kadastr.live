from operator import itemgetter, attrgetter

from django.db import models
from django.contrib.gis.db import models as gis
from django.urls import reverse
import hashlib


class Update(models.Model):

    @classmethod
    def get_latest_update(cls, success=True):
        objects = cls.objects
        if success:
            objects = objects.filter(status=Update.Status.SUCCESS)
        return objects.order_by('-id').first()

    class Status:
        IN_PROGRESS = 'in_progress'
        SUCCESS = 'success'
        ERROR = 'error'

    status = models.CharField(max_length=30, choices=[
        [Status.IN_PROGRESS, Status.IN_PROGRESS],
        [Status.SUCCESS, Status.SUCCESS],
        [Status.ERROR, Status.ERROR]
    ])

    latest_koatuu = models.CharField(default=None, null=True, max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    cadnum = models.CharField(max_length=25)

    address = models.TextField()


class LanduseChange(models.Model):
    class Action:
        CREATE = 'create'
        DELETE = 'delete'
        UPDATE = 'update'

    revision = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='diff_previous')
    previous = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='diff_next')

    cadnum = models.CharField(max_length=25)
    action = models.CharField(
        max_length=10,
        choices=[
            [Action.CREATE, Action.CREATE],
            [Action.DELETE, Action.DELETE],
            [Action.UPDATE, Action.UPDATE],
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)


class Landuse(models.Model):
    OWNERSHIP_TO_NAME = {
        'Комунальна власність': 200,
        'Державна власність': 300,
        'Приватна власність': 100,
        'Не визначено': 0,
    }

    NAME_TO_OWNERSHIP = {
        v: k for k, v in OWNERSHIP_TO_NAME.items()
    }

    cadnum = models.CharField(max_length=25)
    category = models.TextField()
    area = models.TextField()
    unit_area = models.TextField()
    koatuu = models.TextField()
    use = models.TextField()
    purpose = models.TextField()
    purpose_code = models.TextField()
    ownership = models.TextField()
    ownershipcode = models.CharField(max_length=10)

    revision = models.ForeignKey(Update, on_delete=models.CASCADE, db_column='revision')

    point = gis.PointField(null=True)
    bbox = gis.GeometryField(null=True)

    geometry = gis.GeometryField()

    @property
    def address(self):
        try:
            return Address.objects.get(cadnum=self.cadnum).address
        except Address.DoesNotExist:
            return None

    def get_absolute_url(self):
        return reverse('cad_info', kwargs=dict(cad_num=self.cadnum))

    def history(self):
        landuses = Landuse.objects.filter(
            cadnum=self.cadnum,
            koatuu=self.koatuu
        ).distinct(
            'cadnum',
            'category',
            'area',
            'unit_area',
            'koatuu',
            'use',
            'purpose',
            'purpose_code',
            'ownership',
            'ownershipcode',
            'geometry',
        )

        # ordering by creation date
        landuses = list(landuses)
        landuses.sort(key=attrgetter('id'))
        landuses.reverse()
        return landuses

    class Meta:
        managed = False
        db_table = 'landuse'


class Koatuu(models.Model):
    koatuu_id = models.IntegerField()
    name = models.TextField()
    type = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'koatuu'


class SearchIndex(models.Model):
    id = models.TextField(primary_key=True)
    cadnum = models.TextField()

    class Meta:
        managed = False
        db_table = 'test1'
