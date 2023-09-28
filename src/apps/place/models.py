import uuid

from django.db import models

# Create your models here.
from src.apps.brand.models import Brand
from src.apps.hashtag.models import Hashtag
from src.apps.user.models import User


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    latitude = models.DecimalField(max_digits=15, decimal_places=13)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=100, blank=True, null=True)  # TODO nullable false
    telephone = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    hashtags = models.ManyToManyField(Hashtag, blank=True)

    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL, db_column='brand_id')

    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='create_places',
                                   related_query_name='create_place', db_column='created_by_id')
    updated_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='update_places',
                                   related_query_name='update_place', db_column='updated_by_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.name

    @property
    def unique_key(self):
        return '%s-%s-%s' % (self.brand_id, self.address.split()[0], self.name)
