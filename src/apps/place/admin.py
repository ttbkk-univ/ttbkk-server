from django.contrib import admin

# Register your models here.
from django.contrib.admin import display

from src.apps.place.models import Place


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_brand_name', 'latitude', 'longitude', 'created_at', 'updated_at']
    search_fields = ['id', 'name', 'brand__name']

    @display(description='brand_name')
    def get_brand_name(self, obj):
        if obj.brand and obj.brand.name:
            return obj.brand.name
        return ''

    def get_queryset(self, request):
        return Place.objects.select_related('brand')


admin.site.register(Place, PlaceAdmin)
