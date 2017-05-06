from rest_framework.response import Response

from ..base import Endpoint


class FeedEntryIndexEndpoint(Endpoint):
    def get(self, request):
        return Response({})
