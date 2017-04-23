"""
api.views
~~~~~~~~~
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .serializers import EntrySerializer
from .serializers import FeedSerializer
from feeds.managers import FeedEntryManager
from feeds.managers import FeedManager
from feeds.models import Entry
from feeds.models import Feed


class EntryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """API endpoint for viewing, editing Entry objects
    """
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(feed__user=self.request.user)


class FeedViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
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

        _data = serializer.data
        _qs = Feed.objects.filter(user=request.user, id=_data['id'])

        if _qs.exists():
            assert _qs.count() == 1, 'More than one result returned.'

            _feed = _qs.last()
            _entry_mgr = FeedEntryManager(_feed)
            _prepped_entries = [_entry_mgr.prepare(e) for e in _feed_mgr.entries]
            [_entry_mgr.save(p) for p in _prepped_entries]

        headers = self.get_success_headers(_data)

        return Response(_data, status=status.HTTP_201_CREATED, headers=headers)
