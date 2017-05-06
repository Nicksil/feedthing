from django.conf.urls import url

from .endpoints.feed_entry_index import FeedEntryIndexEndpoint
from .endpoints.catchall import CatchallEndpoint
from .endpoints.feed_index import FeedIndexEndpoint

urlpatterns = [
    url(
        r'^feeds/$',
        FeedIndexEndpoint.as_view(),
        name='feedthing-api-v1-feed-index'
    ),
    url(
        r'^feeds/(?P<feed_uid>[^/]+)/entries/$',
        FeedEntryIndexEndpoint.as_view(),
        name='feedthing-api-v1-feed-entry-index'
    ),
    url(
        r'^',
        CatchallEndpoint.as_view(),
        name='feedthing-api-v1-catchall'
    ),
]
