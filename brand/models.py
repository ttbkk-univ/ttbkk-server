from django.db import models


# Create your models here.
from hashtag.models import Hashtag
from user.models import User


class Brand(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    hashtags = models.ManyToManyField(Hashtag)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='create_brands', related_query_name='create_brand')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='update_brands', related_query_name='update_brand')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name
