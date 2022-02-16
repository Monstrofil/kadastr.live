import json
import re

from django.db import connections
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View, ListView
from prometheus_client import generate_latest, Gauge

from cadinfo.models import Landuse, Koatuu, SearchIndex, Update, Address


class LandInfoView(TemplateView):
    template_name = 'cadinfo.html'

    def get_context_data(self, cad_num, **kwargs):
        content = super(LandInfoView, self).get_context_data(**kwargs)
        parcel = get_object_or_404(
            Landuse, cadnum=cad_num,
            revision=Update.get_latest_update().id
        )

        history = Landuse.objects.filter(
            cadnum=cad_num,
            koatuu=parcel.koatuu
        ).distinct('geometry', 'cadnum', 'koatuu', 'purpose', 'ownership', 'use')

        all_parcels = list(history)

        content['land'] = parcel
        content['history'] = list( zip([None, *all_parcels[:-1]], all_parcels))

        return content

    def get_queryset(self):
        pass


class TegolaConfigView(TemplateView):
    template_name = 'tegola.toml'

    def get_context_data(self, **kwargs):
        content = super(TegolaConfigView, self).get_context_data(**kwargs)

        content['updates'] = Update.objects.filter(
            status=Update.Status.SUCCESS
        ).all()

        return content

    def get_queryset(self):
        pass


class ExportGeoJsonView(View):
    def get(self, request, left, bottom, right, top, *args, **kwargs):
        left = float(left)
        bottom = float(bottom)
        right = float(right)
        top = float(top)

        sql = """
            select json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(ST_AsGeoJSON(t.*)::json)
                )
            from ( 
                SELECT 
                    geometry as geometry, 
                    landuse.cadnum, category, purpose_code, purpose, use, area, unit_area, ownershipcode, ownership, landuse.id, address
                FROM landuse 
                LEFT JOIN cadinfo_address ON landuse.cadnum = cadinfo_address.cadnum
                WHERE revision = (
                    SELECT id
                    FROM cadinfo_update
                    WHERE status = 'success'
                    ORDER BY id DESC
                    LIMIT 1
                ) AND geometry && ST_MakeEnvelope(%s,%s,%s,%s, 4326)
            ) as t;
        """
        with connections['default'].cursor() as cursor:
            cursor.execute(sql, [bottom, left, top, right])
            row = cursor.fetchone()
        response = HttpResponse(json.dumps(row[0]), content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=export.geojson'
        return response


class SearchView(View):
    def get(self, request, search, *args, **kwargs):
        results = SearchIndex.objects.raw(
            "SELECT id, cadnum FROM  fulltext WHERE match(%s) LIMIT 10",
            params=(search,)
        )
        landuses = Landuse.objects.filter(cadnum__in=[
            r.cadnum for r in results
        ], revision=Update.get_latest_update()).all()

        results = []
        for landuse in landuses:
            address_info = Address.objects.filter(cadnum=landuse.cadnum).first()
            if address_info and address_info.address not in ["None", ""]:
                address = address_info.address
            else:
                address = None
            results.append({
                'id': landuse.id,
                'cadnum': landuse.cadnum,
                'address': address,
                'area': landuse.area,
                'purpose': landuse.purpose,
                'use': landuse.use,
                'unit_area': landuse.unit_area,
                'location': [landuse.point.x, landuse.point.y]
            })

        response = HttpResponse(json.dumps({
            'results': results
        }), content_type="application/json")
        return response


class MetricsView(View):
    landuse_counter = Gauge('landuse_total', '')
    landuse_processed_counter = Gauge('landuse_processed_total', '')

    def __init__(self):
        super(MetricsView, self).__init__()

    def get(self, request, *args, **kwargs):
        # TODO: refresh this code with optimized queues
        # self.landuse_counter.set(Landuse.objects.count())
        self.landuse_counter.set(-1)
        # self.landuse_processed_counter.set(Landuse.objects.filter(address__isnull=False).count())
        self.landuse_processed_counter.set(-1)
        response = HttpResponse(generate_latest(), content_type="application/json")
        return response


class IndexView(TemplateView):
    template_name = 'index.html'
