from rest_framework.response import Response

from ..base import Endpoint


class EntryDetailsEndpoint(Endpoint):
    def get(self, request, entry_uid=None):
        return Response({})
