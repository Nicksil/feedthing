from django.conf.urls import url, include
from django.views.generic import TemplateView

from feeds import urls as feeds_urls

urlpatterns = [
    url(r'^feeds/', include(feeds_urls, namespace='feeds')),
    url(r'^$', TemplateView.as_view(template_name='index.html'))
]
