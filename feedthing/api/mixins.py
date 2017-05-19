from .serializers.feeds import ContentSerializer
from .serializers.feeds import EntrySerializer
from .serializers.feeds import FeedSerializer
from feeds.models import Content
from feeds.models import Entry
from feeds.models import Feed


class ContentEndpointMixin:
    lookup_field = 'id'
    lookup_url_kwarg = 'content_uid'
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(
            entry__feed__uid=self.kwargs['feed_uid'],
            entry__uid=self.kwargs['entry_uid']
        )


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
