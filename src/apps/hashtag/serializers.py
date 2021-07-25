from rest_framework import serializers

from src.apps.hashtag.models import Hashtag


class HashtagListSerializer(serializers.ListSerializer):
    child = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Hashtag.objects.get_or_create(name=validated_data['name'])


class HashtagResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'
