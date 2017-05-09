from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^import-opml/$',
        views.import_opml,
        name='import_opml'
    ),
    url(
        r'^mark-read/$',
        views.mark_read,
        name='mark_read'
    ),
    url(
        r'^$',
        views.index,
        name='index'
    )
]
