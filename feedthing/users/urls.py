from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^create/$', views.register, name='register'),
    url(r'^authenticate/$', views.authenticate, name='authenticate'),
]
