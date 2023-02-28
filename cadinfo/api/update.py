from django.db.models import Count
from rest_framework import viewsets
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from cadinfo.models import Update, LanduseChange


class LanduseChangeSerialier(ModelSerializer):
    class Meta:
        model = LanduseChange
        exclude = []


class UpdateSerializer(ModelSerializer):
    statistics = SerializerMethodField()

    def get_statistics(self, obj):
        q = obj.diff_previous.values('action').annotate(
            count=Count('action'),
        )
        return {
            item['action']: item['count'] for item in q
        }

    class Meta:
        model = Update
        exclude = ['latest_koatuu']


class UpdateView(viewsets.ReadOnlyModelViewSet):
    queryset = Update.objects.filter(
        status__in=[
            Update.Status.SUCCESS,
            Update.Status.IN_PROGRESS
        ]
    ).order_by('-id')

    serializer_class = UpdateSerializer
    pagination_class = None
