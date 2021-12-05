from django.urls import path
from django.contrib.sitemaps.views import sitemap, index
from django.views.decorators.cache import cache_page
from rest_framework import routers

from .api import ParcelView
from .sitemaps import LanduseSitemap
from .views import LandInfoView, KoatuuInfoView, IndexView, ExportGeoJsonView, LandListView, SearchView, MetricsView

sitemaps = {
    'static': LanduseSitemap,
}

router = routers.SimpleRouter()
router.register(r'api/parcels', ParcelView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/', LandListView.as_view(), name='list'),
    path('metrics/', MetricsView.as_view(), name='metrics'),
    path('parcel/<str:cad_num>', LandInfoView.as_view(), name='cad_info'),
    path('koatuu/<int:koatuu_id>', KoatuuInfoView.as_view()),
    path('export/<left>/<bottom>/<right>/<top>/', ExportGeoJsonView.as_view()),
    path('search/<search>/', SearchView.as_view()),
    path('sitemap.xml', index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', cache_page(3600)(sitemap), {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
] + router.urls
