from django.conf.urls import url, include
from django.views.generic import TemplateView

from api import urls as api_urls
from users import urls as users_urls

urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^users/', include(users_urls, namespace='users')),
    url(r'^register/$', TemplateView.as_view(template_name='register.html'), name='register'),
    url(r'^sign-in/$', TemplateView.as_view(template_name='sign-in.html'), name='sign_in'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]
