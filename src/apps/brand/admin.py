from django.contrib import admin

# Register your models here.
from django.contrib.admin import display
from django.db.models import Count

from src.apps.brand.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_place_count', 'created_at', 'updated_at']
    search_fields = ['name']

    def get_queryset(self, request):
        return Brand.objects.annotate(place_count=Count('place')).order_by('-place_count').all()

    @display(description='place_count')
    def get_place_count(self, obj):
        return obj.place_count


admin.site.register(Brand, BrandAdmin)
