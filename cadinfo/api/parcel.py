import sys
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_filters.backends import ComplexFilterBackend
from rest_framework_gis.serializers import GeoModelSerializer
import rest_framework_filters as filters

from cadinfo.models import Landuse, Update


class NoCountPaginationClass(Paginator):
    @property
    def count(self):
        return sys.maxsize


class ParcelPagination(PageNumberPagination):
    max_page_size = 1000
    page_size_query_param = 'page_size'

    django_paginator_class = NoCountPaginationClass

    # Set any other options you want here like page_size
    def get_paginated_response(self, data):
        return Response(dict(
            next=self.get_next_link(),
            previous=self.get_previous_link(),
            results=data
        ))


class ParcelSerializer(GeoModelSerializer):
    class Meta:
        model = Landuse
        fields = [
            'id',
            'cadnum',
            'geometry',
            'purpose_code',
            'purpose',
        ]


class ManagerFilter(filters.FilterSet):
    class Meta:
        model = Landuse
        fields = {
            'cadnum': ['exact', 'in', 'startswith'],
            'purpose': ['contains']
        }


class ParcelView(viewsets.ReadOnlyModelViewSet):
    queryset = Landuse.objects.filter(
        revision=Update.get_latest_update().id
    ).order_by('id')

    serializer_class = ParcelSerializer
    pagination_class = ParcelPagination

    filter_backends = [ComplexFilterBackend]
    filter_class = ManagerFilter

