from django.db import models


# Create your models here.
class Hashtag(models.Model):
    name = models.CharField(primary_key=True, max_length=150)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name
