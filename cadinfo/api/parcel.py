import logging
import sys
import yaml
from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework_filters.backends import ComplexFilterBackend
from rest_framework_gis.serializers import GeoModelSerializer
import rest_framework_filters as filters

from cadinfo.models import Landuse, Update


class NoCountPaginationClass(Paginator):
    @property
    def count(self):
        try:
            return yaml.load(
                self.object_list.explain(format='YAML'),
                Loader=yaml.SafeLoader
            )[0]['Plan']['Plan Rows']
        except (KeyError, IndexError):
            logging.exception('Unable to estimate query size')
            return 30 * 10**6


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


class RevisionSerializer(ModelSerializer):
    class Meta:
        model = Update
        fields = [
            'id',
            'created_at'
        ]


class ParcelSerializer(GeoModelSerializer):

    revision = RevisionSerializer()

    class Meta:
        model = Landuse
        fields = [
            'id',
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

            'valuation_value',
            'valuation_date',

            'revision',
        ]


class ParcelHistorySerializer(ParcelSerializer):
    history = ParcelSerializer(many=True)
    revision = RevisionSerializer()

    class Meta:
        model = Landuse
        fields = [
            'id',
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
            'address',

            'valuation_value',
            'valuation_date',

            'history',
            'revision',
        ]


class ManagerFilter(filters.FilterSet):
    class Meta:
        model = Landuse
        fields = {
            'cadnum': ['exact', 'in', 'startswith'],
            'purpose': ['contains']
        }


class ParcelView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'cadnum'

    serializer_class = ParcelSerializer
    pagination_class = ParcelPagination

    filter_backends = [ComplexFilterBackend]
    filter_class = ManagerFilter
    
    def list(self, request, *args, **kwargs):
        raise PermissionDenied(detail='Temporary locked')

    def get_queryset(self):
        return Landuse.objects.filter(
            revision=Update.get_latest_update().id
        ).order_by('id')

    @action(detail=True, methods=['get'])
    def history(self, request, cadnum=None):
        parcel = self.get_object()

        serializer = ParcelHistorySerializer(instance=parcel)
        return Response(serializer.data)
