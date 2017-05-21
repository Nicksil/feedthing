from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import RedirectView

from api import urls as api_urls
from feeds import urls as feeds_urls
from users import urls as users_urls


urlpatterns = [
    url(
        r'^api/v1/',
        include(api_urls)
    ),
    url(
        r'^feeds/',
        include(feeds_urls, namespace='feeds')
    ),
    url(
        r'^users/',
        include(users_urls, namespace='users')
    ),
    url(
        r'^$',
        RedirectView.as_view(pattern_name='feeds:index'),
        name='index'
    )
]
