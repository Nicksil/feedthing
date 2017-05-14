from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('users:login'))


urlpatterns = [
    url(
        r'^login/$',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    url(
        r'^logout/$',
        logout_view,
        name='logout'
    ),
]
