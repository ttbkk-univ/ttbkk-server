from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from place.models import Place
from place.serializers import PlaceResponseSerializer, PlaceCreateSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.prefetch_related('hashtags', 'brand__hashtags').all()
    serializer_class = PlaceResponseSerializer

    @transaction.non_atomic_requests
    def create(self, request):
        serializer = PlaceCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            place = serializer.create(request.data)
            response_serializer = PlaceResponseSerializer(place)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid Data'})

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

