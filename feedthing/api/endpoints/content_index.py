from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import ContentEndpointMixin


class ContentIndexEndpoint(ContentEndpointMixin, Endpoint):
    def get(self, request, feed_uid=None, entry_uid=None):
        return Response()
