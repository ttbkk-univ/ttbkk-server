from django.db.models import Count
from rest_framework import viewsets, status, filters
from rest_framework.response import Response

from src.apps.brand.models import Brand
from src.apps.brand.serializers import BrandResponseSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.annotate(place_count=Count('place')).order_by('-place_count').all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'hashtags__name']
    serializer_class = BrandResponseSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
