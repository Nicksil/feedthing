from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import ContentEndpointMixin


class ContentDetailsEndpoint(ContentEndpointMixin, Endpoint):
    def get(self, request, feed_uid=None, entry_uid=None, content_uid=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
