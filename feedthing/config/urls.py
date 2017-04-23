from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView

from api import urls as api_urls

urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]
