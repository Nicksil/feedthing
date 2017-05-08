from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView

from api import urls as api_urls
from feeds import views as feeds_views


def logout_view(request):
    logout(request)
    return redirect('/')

urlpatterns = [
    url(
        r'^api/v1/',
        include(api_urls)
    ),
    url(
        r'^users/login/$',
        LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    url(
        r'^users/logout/$',
        logout_view,
        name='logout'
    ),
    url(
        r'^$',
        feeds_views.index,
        name='index'
    ),
]
