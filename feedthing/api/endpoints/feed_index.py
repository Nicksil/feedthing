from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin
from core.managers import FeedDataManager


class FeedIndexEndpoint(FeedEndpointMixin, Endpoint):
    # noinspection PyUnusedLocal
    def get(self, request):
        feeds = self.get_queryset()
        return Response(self.get_serializer(feeds, many=True).data)

    def post(self, request):
        href = request.data.get('href')
        qs = self.get_queryset()

        if href and not qs.filter(href=href).exists():
            request.data.update(FeedDataManager.fetch(href))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
