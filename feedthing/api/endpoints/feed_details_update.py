from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin
from core.managers import FeedManager
from feeds.models import Entry


class FeedDetailsUpdateEndpoint(FeedEndpointMixin, Endpoint):
    def post(self, request, feed_uid=None):
        feed = self.get_object()
        user = self.request.user
        mgr = FeedManager(feed=feed, user=user)
        feed_data = mgr.fetch_data()
        parsed = mgr.to_dict(feed_data)

        title = parsed.pop('title', '')

        for k, v in parsed.items():
            setattr(feed, k, v)

        if not feed.title:
            feed.title = title

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
