import json

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

import env
from src.apps.place.models import Place
from src.apps.place.serializers import PlaceResponseSerializer, PlaceCreateSerializer, PlacePageResponseSerializer
from src.utils.redis import Redis


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceResponseSerializer

    def list(self, request, *args, **kwargs):
        bottom_left = self.request.query_params.get('bottom_left')
        top_right = self.request.query_params.get('top_right')
        page = self.request.query_params.get('page')
        limit = self.request.query_params.get('limit') or 100
        queryset = self.get_queryset().select_related('brand').prefetch_related('hashtags', 'brand__hashtags')

        if not page or not limit or not bottom_left or not top_right and len(bottom_left.split(',')) != 2 and len(
                top_right.split(',')) != 2:
            return Response(data='page, limit, bottom_left, top_right is required', status=status.HTTP_400_BAD_REQUEST)

        if int(limit) > 200:
            return Response(data='limit must be smaller or equal than 200', status=status.HTTP_400_BAD_REQUEST)

        bottom_left = bottom_left.split(',')
        top_right = top_right.split(',')
        queryset = queryset.filter(latitude__range=(bottom_left[0], top_right[0]),
                                   longitude__range=(bottom_left[1], top_right[1]))

        paginator = Paginator(queryset, limit)
        places = paginator.get_page(page)

        response_serializer = PlaceResponseSerializer(places, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def grid(self, request):
        bottom_left = self.request.query_params.get('bottom_left')
        top_right = self.request.query_params.get('top_right')
        if not bottom_left or not top_right and len(bottom_left.split(',')) != 2 and len(top_right.split(',')) != 2:
            return Response(data='bottom_left, top_right is required', status=status.HTTP_400_BAD_REQUEST)

        redis = Redis.get_client()
        key = 'ttbkk-%s-place-%s' % (env.ENV, hash('%s-%s' % (bottom_left, top_right)))
        cache = redis.get(key)

        if cache:
            return Response(data=json.loads(cache), status=status.HTTP_200_OK)

        [bottom_left_x, bottom_left_y] = bottom_left.split(',')
        [top_right_x, top_right_y] = top_right.split(',')

        if (0.2 > abs(float(bottom_left_y) - float(top_right_y))
            or abs(float(bottom_left_y) - float(top_right_y)) > 1) \
                and (0.2 > abs(float(top_right_x) - float(bottom_left_x))
                     or abs(float(top_right_x) - float(bottom_left_x)) > 1):
            return Response(data='grid size must be smaller or equal than 1', status=status.HTTP_400_BAD_REQUEST)

        bottom_left = bottom_left.split(',')
        top_right = top_right.split(',')

        queryset = self.get_queryset()
        places = queryset.filter(latitude__range=(bottom_left[0], top_right[0]),
                                 longitude__range=(bottom_left[1], top_right[1]))
        count = places.count()

        response_serializer = PlacePageResponseSerializer(dict(edges=places, count=count), many=False)
        redis.set(key, json.dumps(response_serializer.data), ex=60)
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

    @action(detail=False)
    def count(self, request, *args, **kwargs):
        bottom_left = self.request.query_params.get('bottom_left')
        top_right = self.request.query_params.get('top_right')
        queryset = self.get_queryset().select_related('brand').prefetch_related('hashtags', 'brand__hashtags')

        if bottom_left and top_right and len(bottom_left.split(',')) == 2 and len(top_right.split(',')) == 2:
            bottom_left = bottom_left.split(',')
            top_right = top_right.split(',')
            queryset = queryset.filter(latitude__range=(bottom_left[0], top_right[0]),
                                       longitude__range=(bottom_left[1], top_right[1]))

        place_cnt = queryset.count()
        return Response(data=place_cnt, status=status.HTTP_200_OK)
