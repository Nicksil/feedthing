from rest_framework.response import Response

from ..base import Endpoint


class ContentIndexEndpoint(Endpoint):
    def get(self, request, feed_uid=None, entry_uid=None):
        return Response()
