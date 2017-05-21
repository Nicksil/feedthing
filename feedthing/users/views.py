from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.views import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('feeds:index'))
        messages.info(request, 'Username, password mismatch.')
        return redirect(reverse_lazy('users:login'))
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('users:login'))
