from rest_framework import viewsets

from .serializers import FeedSerializer
from feeds.models import Feed


class FeedViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing, editing Feed objects
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
