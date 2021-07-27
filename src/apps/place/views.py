from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from src.apps.place.models import Place
from src.apps.place.serializers import PlaceResponseSerializer, PlaceCreateSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.select_related('brand').prefetch_related('hashtags', 'brand__hashtags').all()
    serializer_class = PlaceResponseSerializer

    def list(self, request, *args, **kwargs):
        bottom_left = self.request.query_params.get('bottom_left')
        top_right = self.request.query_params.get('top_right')
        if bottom_left and top_right and len(bottom_left.split(',')) == 2 and len(top_right.split(',')) == 2:
            bottom_left = bottom_left.split(',')
            top_right = top_right.split(',')
            queryset = Place.objects.filter(latitude__range=(bottom_left[0], top_right[0]),
                                            longitude__range=(bottom_left[1], top_right[1])).prefetch_related(
                'hashtags', 'brand__hashtags').all()
        else:
            queryset = self.get_queryset()
        response_serializer = PlaceResponseSerializer(queryset, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

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

