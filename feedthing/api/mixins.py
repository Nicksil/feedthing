from .serializers.feeds import EntrySerializer
from .serializers.feeds import FeedSerializer
from feeds.models import Entry
from feeds.models import Feed


class EntryEndpointMixin:
    lookup_field = 'uid'
    lookup_url_kwarg = 'entry_uid'
    serializer_class = EntrySerializer

    def get_queryset(self):
        return Entry.objects.filter(feed__uid=self.kwargs['feed_uid'])


class FeedEndpointMixin:
    lookup_field = 'uid'
    lookup_url_kwarg = 'feed_uid'
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)
