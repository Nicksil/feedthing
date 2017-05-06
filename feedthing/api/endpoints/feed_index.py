from rest_framework.response import Response

from ..base import Endpoint
from ..serializers.feeds import FeedSerializer


class FeedIndexEndpoint(Endpoint):
    def get(self, request):
        return Response(
            FeedSerializer(
                request.user.feeds.all(),
                context={'request': request},
                many=True,
            ).data
        )

    def post(self, request):
        serializer = FeedSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
