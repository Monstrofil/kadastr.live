from django.db import models
from django.contrib.gis.db import models as gis
from django.urls import reverse
import hashlib


class Landuse(models.Model):
    cadnum = models.TextField()
    category = models.TextField()
    area = models.TextField()
    unit_area = models.TextField()
    koatuu = models.TextField()
    use = models.TextField()
    purpose = models.TextField()
    purpose_code = models.TextField()
    ownership = models.TextField()
    ownershipcode = models.TextField()
    address = models.TextField()

    created_at = models.BigIntegerField()

    point = gis.PointField(null=True)
    bbox = gis.GeometryField(null=True)

    geometry = gis.GeometryField()

    hash = models.CharField(max_length=255, default='')

    def get_hash(self):
        return hashlib.md5(
            ';'.join([
                self.cadnum,
                self.area,
                self.unit_area,
                self.koatuu,
                self.use,
                self.purpose,
                self.purpose_code,
                self.ownership,
                self.address,
            ]).encode()
        ).hexdigest()

    def get_absolute_url(self):
        return reverse('cad_info', kwargs=dict(cad_num=self.cadnum))

    class Meta:
        managed = False
        db_table = 'landuse'


class Koatuu(models.Model):
    koatuu_id = models.IntegerField()
    name = models.TextField()
    type = models.CharField(max_length=2)

    # parent = models.ForeignKey('self', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'koatuu'


class SearchIndex(models.Model):
    id = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'test1'
