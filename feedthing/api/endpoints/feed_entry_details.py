from rest_framework.response import Response

from ..base import Endpoint


class FeedEntryDetailsEndpoint(Endpoint):
    def get(self, request, entry_uid=None):
        return Response({})
