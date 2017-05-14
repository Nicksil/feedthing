from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<feed_uid>[^/]+)/$',
        views.detail,
        name='detail'
    ),
    url(
        r'^(?P<feed_uid>[^/]+)/update/$',
        views.update,
        name='update'
    ),
    url(
        r'^$',
        views.index,
        name='index'
    )
]
