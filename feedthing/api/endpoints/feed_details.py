from rest_framework.response import Response

from ..base import Endpoint
from ..exceptions import ResourceDoesNotExist
from ..serializers.feeds import FeedSerializer
from feeds.models import Feed


class FeedDetailsEndpoint(Endpoint):
    def get(self, request, feed_slug=None):
        try:
            feed = Feed.objects.get(slug=feed_slug, users=request.user)
        except Feed.DoesNotExist:
            raise ResourceDoesNotExist
        return Response(FeedSerializer(feed).data)
