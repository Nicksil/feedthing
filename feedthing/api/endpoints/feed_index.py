from rest_framework.response import Response

from feeds.managers import FeedManager
from feeds.models import Entry
from ..base import Endpoint
from ..mixins import FeedEndpointMixin


class FeedIndexEndpoint(FeedEndpointMixin, Endpoint):
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        query_dict = request.data.copy()

        href = request.data.get('href')
        mgr = FeedManager(href)
        qs = self.get_queryset()

        if href and not qs.filter(href=href).exists():
            data = mgr.fetch_data()
            query_dict.update(mgr.to_dict(data))

        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        feed = serializer.save()
        mgr.feed = feed
        [Entry.objects.create(**e) for e in mgr.entries]
        serializer = self.get_serializer(feed)
        return Response(serializer.data)
