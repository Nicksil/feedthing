from rest_framework.response import Response

from core.managers import FeedDataManager
from feeds.models import Entry
from ..base import Endpoint
from ..mixins import FeedEndpointMixin


class FeedDetailsEndpoint(FeedEndpointMixin, Endpoint):
    # noinspection PyUnusedLocal
    def get(self, request, feed_uid=None):
        feed = self.get_object()
        serializer = self.get_serializer(feed)
        return Response(serializer.data)


class FeedDetailsUpdateEndpoint(FeedEndpointMixin, Endpoint):
    # noinspection PyUnusedLocal
    def post(self, request, feed_uid=None):
        feed = self.get_object()
        user = self.request.user
        mgr = FeedDataManager(feed=feed, user=user)
        feed_data = mgr.fetch_data()
        parsed = mgr.to_internal(feed_data)

        for k, v in parsed.items():
            setattr(feed, k, v)

        feed.save()

        entries = mgr.entries

        for entry in entries:
            if not Entry.objects.filter(href=entry['href'], feed=feed).exists():
                _new = Entry.objects.create(**entry)
            else:
                _existing = Entry.objects.get(href=entry['href'], feed=feed)

                for k, v in entry.items():
                    setattr(_existing, k, v)

                _existing.save()

        serializer = self.get_serializer(feed)

        return Response(serializer.data)
