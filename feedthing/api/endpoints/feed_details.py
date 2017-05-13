from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin


class FeedDetailsEndpoint(FeedEndpointMixin, Endpoint):
    def get(self, request, feed_uid=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
