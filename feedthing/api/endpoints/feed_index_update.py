import threading

from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin
from core.managers import FeedDataManager
from feeds.models import Entry


def _handle(feed, user):
    mgr = FeedDataManager(feed=feed, user=user)
    feed_data = mgr.fetch_data()
    parsed = mgr.to_internal(feed_data)

    deleted_count = 0
    if mgr.data.get('status', None) == 404:
        feed.delete()
        deleted_count += 1

    for k, v in parsed.items():
        setattr(feed, k, v)
    feed.save()

    entries = mgr.entries

    for entry in entries:
        if not Entry.objects.filter(href=entry['href'], feed=feed).exists():
            Entry.objects.create(**entry)
        else:
            _existing = Entry.objects.get(href=entry['href'], feed=feed)

            for k, v in entry.items():
                setattr(_existing, k, v)
            _existing.save()


class FeedIndexUpdateEndpoint(FeedEndpointMixin, Endpoint):
    def post(self, request, feed_uid=None):
        feeds = self.get_queryset()
        user = self.request.user

        for feed in feeds:
            t = threading.Thread(target=_handle, args=(feed, user))
            t.start()

        feeds = self.get_queryset()
        serializer = self.get_serializer(feeds, many=True)

        return Response(serializer.data)
