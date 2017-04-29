from rest_framework import viewsets

from ..models import User
from .serializers import UserHyperlinkedModelSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserHyperlinkedModelSerializer
