from rest_framework.response import Response

from ..base import Endpoint
from ..serializers.feeds import FeedSerializer


class FeedIndexEndpoint(Endpoint):
    def get(self, request):
        return Response(
            FeedSerializer(
                request.user.feeds.all(),
                many=True,
            ).data
        )
