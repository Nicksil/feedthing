from rest_framework import viewsets

from ..models import Entry
from ..models import Feed
from .serializers import EntryHyperlinkedModelSerializer
from .serializers import FeedHyperlinkedModelSerializer


class EntryAPIViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntryHyperlinkedModelSerializer


class FeedAPIViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedHyperlinkedModelSerializer
