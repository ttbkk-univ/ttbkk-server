from django.db import models


# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True)
    nickname = models.CharField(max_length=50)
    social_id = models.CharField(max_length=50)
    social_type = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.nickname
