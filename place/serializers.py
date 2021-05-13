import json

from rest_framework import serializers

from brand.models import Brand
from brand.serializers import BrandResponseSerializer
from hashtag.models import Hashtag
from hashtag.serializers import HashtagResponseSerializer, HashtagListSerializer
from place.models import Place
from user.models import User


class PlaceResponseSerializer(serializers.ModelSerializer):
    brand = BrandResponseSerializer(many=False, read_only=True)
    hashtags = HashtagResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'


class PlaceCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    description = serializers.CharField(max_length=500, allow_null=True)
    brand_name = serializers.CharField(max_length=150, allow_null=True)
    hashtags = HashtagListSerializer()

    def create(self, validated_data):
        brand, created = Brand.objects.get_or_create(name=validated_data['brand_name'])
        hashtags = []
        for name in validated_data['hashtags']:
            hashtag, created = Hashtag.objects.get_or_create(name=name)
            hashtags.append(hashtag)
        place = Place.objects.create(name=validated_data['name'], latitude=validated_data['latitude'],
                                     longitude=validated_data['longitude'], description=validated_data['description'],
                                     brand=brand)
        for hashtag in hashtags:
            place.hashtags.add(hashtag)
        return place

    def update(self, instance, validated_data):
        pass
