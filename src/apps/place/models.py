import uuid

from django.db import models

# Create your models here.
from src.apps.brand.models import Brand
from src.apps.hashtag.models import Hashtag
from src.apps.user.models import User


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='create_places',
                                   related_query_name='create_place')
    updated_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='update_places',
                                   related_query_name='update_place')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
