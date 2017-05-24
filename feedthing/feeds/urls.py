from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),
    url(
        r'^add/$',
        views.add_feed,
        name='add_feed'
    ),
    url(
        r'^(?P<feed_id>[^/]+)/$',
        views.detail,
        name='detail'
    ),
    url(
        r'^(?P<feed_id>[^/]+)/fetch/$',
        views.fetch,
        name='fetch'
    ),
    url(
        r'^(?P<feed_id>[^/]+)/delete/$',
        views.delete,
        name='delete'
    ),
    url(
        r'^(?P<feed_id>[^/]+)/edit/$',
        views.edit,
        name='edit'
    ),
    url(
        r'^(?P<feed_id>[^/]+)/entries/(?P<entry_id>[^/]+)/$',
        views.entry,
        name='entry'
    ),
]
