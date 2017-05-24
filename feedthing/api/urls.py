from django.conf.urls import url

from .endpoints.catchall import CatchallEndpoint
from .endpoints.entry_details import EntryDetailsEndpoint
from .endpoints.entry_index import EntryIndexEndpoint
from .endpoints.feed_details import FeedDetailsEndpoint
from .endpoints.feed_index import FeedIndexEndpoint

urlpatterns = [
    url(
        r'^feeds/$',
        FeedIndexEndpoint.as_view(),
        name='feedthing-api-v1-feed-index'
    ),
    url(
        r'^feeds/(?P<feed_id>[^/]+)/$',
        FeedDetailsEndpoint.as_view(),
        name='feedthing-api-v1-feed-details'
    ),
    url(
        r'^feeds/(?P<feed_id>[^/]+)/entries/$',
        EntryIndexEndpoint.as_view(),
        name='feedthing-api-v1-entry-index'
    ),
    url(
        r'^feeds/(?P<feed_id>[^/]+)/entries/(?P<entry_id>[^/]+)/$',
        EntryDetailsEndpoint.as_view(),
        name='feedthing-api-v1-entry-details'
    ),
    url(
        r'^',
        CatchallEndpoint.as_view(),
        name='feedthing-api-v1-catchall'
    ),
]
