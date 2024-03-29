from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from src.apps.brand.models import Brand
from src.apps.brand.serializers import BrandResponseSerializer, BrandResponseForPlaceSerializer
from src.apps.hashtag.models import Hashtag
from src.apps.hashtag.serializers import HashtagResponseSerializer, HashtagListSerializer
from src.apps.place.models import Place


class PlaceResponseSerializer(serializers.ModelSerializer):
    brand = BrandResponseForPlaceSerializer(many=False, read_only=True)
    hashtags = HashtagResponseSerializer(many=True, read_only=True)
    longitude = SerializerMethodField()
    latitude = SerializerMethodField()

    class Meta:
        model = Place
        fields = '__all__'

    @staticmethod
    def get_longitude(obj):
        return float(obj.longitude)

    @staticmethod
    def get_latitude(obj):
        return float(obj.latitude)


class PlaceSimpleResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    name = serializers.CharField()
    brand_id = serializers.UUIDField()
    brand = BrandResponseForPlaceSerializer(many=False, read_only=True)
    hashtags = HashtagResponseSerializer(many=True, read_only=True)


class PlacePageResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    edges = PlaceSimpleResponseSerializer(many=True, read_only=True)


class PlaceCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    description = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)
    brand_name = serializers.CharField(max_length=150, allow_blank=True, allow_null=True)
    hashtags = HashtagListSerializer(allow_empty=True, allow_null=True)

    def create(self, validated_data):
        brand_name_input = validated_data.get('brand_name')
        brand = None
        if brand_name_input:
            brand, created = Brand.objects.get_or_create(name=brand_name_input)

        hashtags_input = validated_data.get('hashtags')
        hashtags = []
        if hashtags_input:
            for name in hashtags_input:
                hashtag, created = Hashtag.objects.get_or_create(name=name)
                hashtags.append(hashtag)

        place = Place.objects.create(
            name=validated_data['name'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            description=validated_data['description'],
            brand=brand,
        )

        for hashtag in hashtags:
            place.hashtags.add(hashtag)

        return place

    def update(self, instance, validated_data):
        pass
