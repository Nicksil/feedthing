from django.contrib.auth import authenticate as _authenticate, logout
from django.contrib.auth import login
from django.shortcuts import redirect

from users.models import User


def register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    User.objects.create_user(email=email, password=password)

    return authenticate(request)


def authenticate(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = _authenticate(email=email, password=password)

    if user is not None:
        login(request, user)

    return redirect('index')


def sign_out(request):
    logout(request)
    return redirect('index')
