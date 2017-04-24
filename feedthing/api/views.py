"""
api.views
~~~~~~~~~
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import EntrySerializer
from .serializers import FeedSerializer
from feeds.managers import FeedManager
from feeds.models import Entry
from feeds.models import Feed


class EntryViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Entry objects
    """
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(feed__user=self.request.user)


class FeedViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Feed objects
    """
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        _feed_mgr = FeedManager(request.user, href=request.data['href'])
        _fetched = _feed_mgr.fetch()
        _prepped = _feed_mgr.prepare(_fetched)

        serializer = self.get_serializer(data=_prepped)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
