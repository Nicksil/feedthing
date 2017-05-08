from rest_framework import status
from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import EntryEndpointMixin


class EntryDetailsEndpoint(EntryEndpointMixin, Endpoint):
    # noinspection PyUnusedLocal
    def get(self, request, feed_uid=None, entry_uid=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    # noinspection PyUnusedLocal
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # noinspection PyUnusedLocal
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # noinspection PyUnusedLocal
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
