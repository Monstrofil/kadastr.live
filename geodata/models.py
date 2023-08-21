from django.contrib.gis.db import models as gis
from django.db import models


class GeoJsonUpload(models.Model):
    """
    Represents single geojson upload to be processed
    by django and added to database
    """
    content_hash = models.CharField(max_length=32)
    filename = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)


class GeoRecord(models.Model):
    """
    Represents single geometry record with information about
    it's attributes and date of creation
    """
    group = models.CharField(max_length=255)

    geometry = gis.GeometryField(srid=4326)

    geometry_zoom_8 = gis.GeometryField(srid=4326)
    geometry_zoom_10 = gis.GeometryField(srid=4326)
    geometry_zoom_12 = gis.GeometryField(srid=4326)
    properties = models.JSONField()

    revision = models.ForeignKey(
        GeoJsonUpload, on_delete=models.CASCADE)
