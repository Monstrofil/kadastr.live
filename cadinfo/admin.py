from django.contrib import admin
from .models import Landuse, Update


@admin.register(Landuse)
class LanduseModelAdmin(admin.ModelAdmin):
    show_full_result_count = False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ('cadnum', 'purpose', 'revision')


@admin.register(Update)
class UpdateModelAdmin(admin.ModelAdmin):
    show_full_result_count = False

    list_display = ('id', 'status')
