from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin
from core.managers import FeedDataManager
from feeds.models import Entry


class FeedIndexEndpoint(FeedEndpointMixin, Endpoint):
    # noinspection PyUnusedLocal
    def get(self, request):
        feeds = self.get_queryset()
        return Response(self.get_serializer(feeds, many=True).data)

    def post(self, request):
        href = request.data.get('href')
        mgr = FeedDataManager(href)
        qs = self.get_queryset()

        if href and not qs.filter(href=href).exists():
            data = mgr.fetch_data()
            request.data.update(mgr.to_internal(data))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feed = serializer.save()
        mgr.feed = feed
        [Entry.objects.create(**e) for e in mgr.entries]
        serializer = self.get_serializer(feed)

        return Response(serializer.data)
