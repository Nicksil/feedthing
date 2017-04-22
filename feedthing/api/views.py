from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .serializers import FeedSerializer
from feeds.managers import FeedEntryManager
from feeds.models import Feed


class FeedViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Feed objects
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)

    @detail_route(methods=['post', 'put'])
    def fetch(self, request, pk=None):
        obj = self.get_object()
        result = FeedEntryManager.fetch_and_save(obj)
        # ------------- PDEBUG -------------
        print('=' * 100)
        print(result)
        print('=' * 100)
        # ------------- PDEBUG -------------
        return Response(status=status.HTTP_200_OK)
