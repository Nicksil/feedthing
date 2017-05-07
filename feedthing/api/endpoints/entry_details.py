from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import EntryEndpointMixin


class EntryDetailsEndpoint(EntryEndpointMixin, Endpoint):
    def get(self, request, feed_uid=None, entry_uid=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
