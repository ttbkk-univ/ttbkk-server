from django.contrib import admin

# Register your models here.
from place.models import Place


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'latitude', 'longitude']


admin.site.register(Place, PlaceAdmin)
