from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import EntryEndpointMixin


class EntryIndexEndpoint(EntryEndpointMixin, Endpoint):
    # noinspection PyUnusedLocal
    def get(self, request, feed_uid=None):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
