from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin
from feeds.managers import FeedManager


class FeedIndexEndpoint(FeedEndpointMixin, Endpoint):
    def get(self, request):
        feeds = self.get_queryset().order_by('title')
        serializer = self.get_serializer(feeds, many=True)
        return Response(serializer.data)

    def post(self, request):
        href = request.data.get('href')
        mgr = FeedManager(href=href, user=request.user)
        feed = mgr.create()
        serializer = self.get_serializer(feed)
        return Response(serializer.data)
