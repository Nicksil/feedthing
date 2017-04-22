from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import EntrySerializer
from .serializers import FeedSerializer
from feeds.models import Entry
from feeds.models import Feed


class FeedViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Feed objects
    """
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)


class EntryViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Entry objects
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
