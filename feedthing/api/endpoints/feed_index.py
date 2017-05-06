from rest_framework.response import Response

from ..base import Endpoint


class FeedIndexEndpoint(Endpoint):
    def get(self, request):
        return Response({})
