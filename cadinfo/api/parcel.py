import sys
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_gis.serializers import GeoModelSerializer

from cadinfo.models import Landuse


class NoCountPaginationClass(Paginator):
    def count(self):
        return sys.maxsize


class ParcelPagination(PageNumberPagination):
    max_page_size = 1000

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
        fields = ['id', 'cadnum', 'geometry', 'created_at', 'deleted_at']


class ParcelView(viewsets.ReadOnlyModelViewSet):
    queryset = Landuse.objects.filter(deleted_at__isnull=True).order_by('id')

    serializer_class = ParcelSerializer
    pagination_class = ParcelPagination
