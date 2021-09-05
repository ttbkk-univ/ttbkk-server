from django.contrib import admin

# Register your models here.
from src.apps.place.models import Place


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'latitude', 'longitude']
    search_fields = ['id', 'name', 'brand__name']


admin.site.register(Place, PlaceAdmin)
