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
        r'^(?P<feed_uid>[^/]+)/$',
        views.detail,
        name='detail'
    ),
    url(
        r'^(?P<feed_uid>[^/]+)/fetch/$',
        views.fetch,
        name='fetch'
    ),
    url(
        r'^(?P<feed_uid>[^/]+)/delete/$',
        views.delete,
        name='delete'
    ),
    url(
        r'^(?P<feed_uid>[^/]+)/edit/$',
        views.edit,
        name='edit'
    ),
]
