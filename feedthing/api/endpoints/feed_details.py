from rest_framework import status
from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin
from feeds.managers import FeedManager


class FeedDetailsEndpoint(FeedEndpointMixin, Endpoint):
    def get(self, request, feed_id=None):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def delete(self, request, feed_id=None):
        feed = self.get_object()
        feed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def post(self, request, feed_id=None):
        feed = self.get_object()
        mgr = FeedManager(feed=feed)
        serializer = self.get_serializer(mgr.update())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
