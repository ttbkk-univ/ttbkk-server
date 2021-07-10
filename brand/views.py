from rest_framework import viewsets, status, filters, generics, mixins
from brand.models import Brand
from brand.serializers import BrandResponseSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.prefetch_related('hashtags').all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'hashtags__name']
    serializer_class = BrandResponseSerializer