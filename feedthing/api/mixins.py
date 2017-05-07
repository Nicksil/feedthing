from .serializers.feeds import FeedSerializer
from feeds.models import Feed


class FeedEndpointMixin:
    lookup_field = 'uid'
    lookup_url_kwarg = 'feed_uid'
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)
