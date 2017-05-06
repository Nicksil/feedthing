from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView

from api import urls as api_urls
from entries import urls as entries_urls
from feeds import urls as feeds_urls


def logout_view(request):
    logout(request)
    return redirect('/')

urlpatterns = [
    url(r'^api/v1/', include(api_urls)),
    url(r'^entries/', include(entries_urls)),
    url(r'^feeds/', include(feeds_urls)),
    url(r'^users/login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^users/logout/$', logout_view, name='logout'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]
