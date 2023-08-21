from django.contrib import admin

from geodata.models import GeoJsonUpload, GeoRecord

admin.site.register(GeoJsonUpload)
admin.site.register(GeoRecord)