from django.shortcuts import render, redirect

import feedparser

from .models import Feed


def index(request):
    context = {'feeds': request.user.feeds.all()}
    return render(request, 'feeds/index.html', context=context)


def add_feed(request):
    url = request.POST.get('url')
    parsed = feedparser.parse(url)
    href = parsed['href']
    title = parsed['feed']['title']

    Feed.objects.create(
        href=href,
        title=title,
        user=request.user
    )

    return redirect('feeds:index')
