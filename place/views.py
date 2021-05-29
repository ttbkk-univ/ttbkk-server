from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from place.models import Place
from place.serializers import PlaceResponseSerializer, PlaceCreateSerializer


class PlaceViewSet(viewsets.ViewSet):
    queryset = Place.objects.all()

    @transaction.non_atomic_requests
    def create(self, request):
        serializer = PlaceCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            place = serializer.create(request.data)
            response_serializer = PlaceResponseSerializer(place)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid Data'})

    def list(self, request):
        places = Place.objects.all()
        response_serializer = PlaceResponseSerializer(places, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
