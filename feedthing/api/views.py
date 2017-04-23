from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .serializers import EntrySerializer
from .serializers import FeedSerializer
from feeds.managers import FeedEntryManager
from feeds.models import Entry
from feeds.models import Feed


class EntryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    api.views.EntryViewSet
    ~~~~~~~~~~~~~~~~~~~~~~
    
    API endpoint for viewing, editing Entry objects
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class FeedViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    api.views.FeedViewSet
    ~~~~~~~~~~~~~~~~~~~~~~
    
    API endpoint for viewing, editing Feed objects
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)

    # noinspection PyUnusedLocal
    @detail_route(methods=['post', 'put'])
    def fetch(self, *args, **kwargs):
        obj = self.get_object()
        FeedEntryManager.fetch_and_save(obj)

        return Response(status=status.HTTP_200_OK)
