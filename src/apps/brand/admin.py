from django.contrib import admin

# Register your models here.
from src.apps.brand.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    search_fields = ['name']


admin.site.register(Brand)
