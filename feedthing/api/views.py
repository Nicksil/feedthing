"""
api.views
~~~~~~~~~
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .serializers import EntrySerializer
from .serializers import FeedSerializer
from feeds.managers import FeedEntryManager, FeedManager
from feeds.models import Entry
from feeds.models import Feed


class EntryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """API endpoint for viewing, editing Entry objects
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class FeedViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """API endpoint for viewing, editing Feed objects
    """
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Feed Manager
        _mgr = FeedManager(request.user, href=request.data['href'])
        _fetched = _mgr.fetch()
        _prepped = _mgr.prepare(_fetched)

        serializer = self.get_serializer(data=_prepped)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # noinspection PyUnusedLocal
    @detail_route(methods=['post', 'put'])
    def fetch(self, *args, **kwargs):
        obj = self.get_object()
        FeedEntryManager.fetch_and_save(obj)

        return Response(status=status.HTTP_200_OK)
