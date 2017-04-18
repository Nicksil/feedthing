from django.conf.urls import include
from django.conf.urls import url

from feeds import urls as feeds_urls

urlpatterns = [
    url(r'^', include(feeds_urls, namespace='feeds'))
]
