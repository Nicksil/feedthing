from rest_framework.response import Response

from ..base import Endpoint


class EntryIndexEndpoint(Endpoint):
    def get(self, request):
        return Response({})
