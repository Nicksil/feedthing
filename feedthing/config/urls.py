from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView

from api import urls as api_urls
from entries import urls as entries_urls
from feeds import urls as feeds_urls
from users import urls as users_urls

urlpatterns = [
    url(r'^api/v1/', include(api_urls)),
    url(r'^entries/', include(entries_urls)),
    url(r'^feeds/', include(feeds_urls)),
    url(r'^users/', include(users_urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]
