from rest_framework import viewsets

from .serializers import EntrySerializer
from .serializers import FeedSerializer
from feeds.models import Entry
from feeds.models import Feed


class FeedViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Feed objects
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class EntryViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Entry objects
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
