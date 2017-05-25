from rest_framework import status as http_status
from rest_framework.response import Response

from ..base import Endpoint
from ..mixins import FeedEndpointMixin
from core.exceptions import FeedManagerError
from feeds.managers import FeedManager


class FeedIndexEndpoint(FeedEndpointMixin, Endpoint):
    def get(self, request):
        feeds = self.get_queryset().order_by('title')
        serializer = self.get_serializer(feeds, many=True)
        return Response(serializer.data)

    def post(self, request):
        href = request.data.get('href')

        if not href:
            data = {'error': 'Must provide value for `href`.'}
            status = http_status.HTTP_400_BAD_REQUEST
        else:
            try:
                mgr = FeedManager(href=href, user=request.user)
                feed = mgr.create()
                serializer = self.get_serializer(feed)
                data = serializer.data
                status = http_status.HTTP_201_CREATED
            except FeedManagerError as e:
                data = {'error': str(e)}
                status = http_status.HTTP_400_BAD_REQUEST

        return Response(data, status=status)
