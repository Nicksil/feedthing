from rest_framework import viewsets

from ..models import Feed
from .serializers import FeedHyperlinkedModelSerializer


class FeedAPIViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedHyperlinkedModelSerializer
