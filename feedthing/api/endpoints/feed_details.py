from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin


class FeedDetailsEndpoint(FeedEndpointMixin, Endpoint):
    # noinspection PyUnusedLocal
    def get(self, request, feed_uid=None):
        feed = self.get_object()
        serializer = self.get_serializer(feed)
        return Response(serializer.data)
