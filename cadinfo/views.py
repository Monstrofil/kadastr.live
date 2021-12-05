import json

from django.db import connection, connections
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView, View, ListView
from prometheus_client import CollectorRegistry, generate_latest, Metric, Gauge

from cadinfo.models import Landuse, Koatuu, SearchIndex


class LandInfoView(TemplateView):
    template_name = 'cadinfo.html'

    def get_context_data(self, cad_num, **kwargs):
        content = super(LandInfoView, self).get_context_data(**kwargs)
        content['land'] = get_object_or_404(Landuse, cadnum=cad_num)

        return content

    def get_queryset(self):
        pass


class LandListView(ListView):
    paginate_by = 100
    model = Landuse
    ordering = 'cadnum'
    template_name = 'list.html'

    def get_queryset(self):
        return super(LandListView, self).get_queryset()


class KoatuuInfoView(TemplateView):
    template_name = 'koatuu.html'

    def get_context_data(self, koatuu_id, **kwargs):
        content = super(KoatuuInfoView, self).get_context_data(**kwargs)
        content['koatuu'] = get_object_or_404(Koatuu, koatuu_id=koatuu_id)

        content['lands'] = Landuse.objects.filter(koatuu=str(koatuu_id))

        return content


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
                    ST_Transform(point, 4326) as point, 
                    cadnum, category, purpose_code, purpose, use, area, unit_area, ownershipcode, ownership, id, address
                FROM landuse 
                WHERE point && ST_Transform(ST_MakeEnvelope(%s,%s,%s,%s, 4326), 3857)
            ) as t;
        """
        with connections['cadastre'].cursor() as cursor:
            cursor.execute(sql, [bottom, left, top, right])
            row = cursor.fetchone()
        response = HttpResponse(json.dumps(row[0]), content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=export.geojson'
        return response


class SearchView(View):
    def get(self, request, search, *args, **kwargs):
        searchBy = request.GET.get('searchBy', 'address')
        if searchBy == 'address':
            results = SearchIndex.objects.raw(
                "SELECT id FROM test1 WHERE match(%s) LIMIT 10",
                params=(search,)
            )
        elif searchBy == 'usage':
            results = SearchIndex.objects.raw(
                "SELECT id FROM usage_index WHERE match(%s) LIMIT 10",
                params=(search,)
            )
        else:
            return HttpResponse(status_code=400)
        landuses = Landuse.objects.filter(id__in=[r.id for r in results]).all()

        results = []
        for landuse in landuses:
            landuse.point.transform(3857)
            results.append({
                'id': landuse.id,
                'value': landuse.address if searchBy == 'address' else landuse.use,
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
