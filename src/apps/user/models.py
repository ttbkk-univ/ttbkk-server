import uuid

from django.db import models


# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nickname = models.CharField(max_length=50)
    social_id = models.CharField(max_length=50)
    social_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.nickname
