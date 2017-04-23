"""
users.views
~~~~~~~~~~~
"""

from django.contrib.auth import authenticate as _authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect

from .models import User


def register(request):
    """Create a single User object.
    """

    email = request.POST.get('email')
    password = request.POST.get('password')
    User.objects.create_user(email=email, password=password)

    return authenticate(request)


def authenticate(request):
    """'Sign-in' a user, creating their session.
    """

    email = request.POST.get('email')
    password = request.POST.get('password')
    user = _authenticate(email=email, password=password)

    if user is not None:
        login(request, user)

    return redirect('index')


def sign_out(request):
    """'Sign-out' a user, destroying their session.
    """

    logout(request)
    return redirect('index')
