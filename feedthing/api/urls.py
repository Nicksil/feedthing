from django.conf.urls import url

from .endpoints.catchall import CatchallEndpoint
from .endpoints.content_details import ContentDetailsEndpoint
from .endpoints.content_index import ContentIndexEndpoint
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
        r'^feeds/(?P<feed_uid>[^/]+)/$',
        FeedDetailsEndpoint.as_view(),
        name='feedthing-api-v1-feed-details'
    ),
    url(
        r'^feeds/(?P<feed_uid>[^/]+)/entries/$',
        EntryIndexEndpoint.as_view(),
        name='feedthing-api-v1-entry-index'
    ),
    url(
        r'^feeds/(?P<feed_uid>[^/]+)/entries/(?P<entry_uid>[^/]+)/$',
        EntryDetailsEndpoint.as_view(),
        name='feedthing-api-v1-entry-details'
    ),
    url(
        r'^feeds/(?P<feed_uid>[^/]+)/entries/(?P<entry_uid>[^/]+)/content/$',
        ContentIndexEndpoint.as_view(),
        name='feedthing-api-v1-content-index'
    ),
    url(
        r'^feeds/(?P<feed_uid>[^/]+)/entries/(?P<entry_uid>[^/]+)/content/(?P<content_uid>[^/]+)/$',
        ContentDetailsEndpoint.as_view(),
        name='feedthing-api-v1-content-details'
    ),
    url(
        r'^',
        CatchallEndpoint.as_view(),
        name='feedthing-api-v1-catchall'
    ),
]
