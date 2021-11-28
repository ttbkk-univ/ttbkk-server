from django.contrib import admin

# Register your models here.
from src.apps.hashtag.models import Hashtag


class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


admin.site.register(Hashtag)
