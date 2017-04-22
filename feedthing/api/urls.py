from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^authenticate/$', views.authenticate, name='authenticate'),
    url(r'^create/$', views.register, name='register'),
    url(r'^sign-out/$', views.sign_out, name='sign_out'),
]
