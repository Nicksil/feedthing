from django.shortcuts import render


def add_feed(request):
    return render(request, 'index.html')
