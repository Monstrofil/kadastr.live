from django.db import models
from django.contrib.gis.db import models as gis
from django.urls import reverse
import hashlib


class Update(models.Model):

    @classmethod
    def get_latest_update(cls):
        return cls.objects.order_by('-id').first()

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

    def get_absolute_url(self):
        return reverse('cad_info', kwargs=dict(cad_num=self.cadnum))

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
