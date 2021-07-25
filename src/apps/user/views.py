from rest_framework import viewsets

from src.apps.user.models import User
from src.apps.user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
