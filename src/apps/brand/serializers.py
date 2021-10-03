from rest_framework import serializers
from src.apps.brand.models import Brand
from src.apps.hashtag.serializers import HashtagResponseSerializer


class BrandResponseSerializer(serializers.ModelSerializer):
    hashtags = HashtagResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'
