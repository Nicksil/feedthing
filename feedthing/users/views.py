from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect


def sign_in(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)

    return redirect('/')
