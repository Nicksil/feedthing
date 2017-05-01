from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render

import feedparser

from .api.serializers import FeedHyperlinkedModelSerializer
from .models import Feed
from core.parsers import EntryParser
from core.parsers import FeedParser
from entries.api.serializers import EntryHyperlinkedModelSerializer


def index(request):
    payload = {}
    user = request.user

    if user.is_authenticated:
        feeds = user.feeds.all()
        serializer = FeedHyperlinkedModelSerializer(feeds, context={'request': request}, many=True)
        payload = {'feeds': serializer.data}

    return render(request, 'index.html', payload)


def add(request):
    feed_data = feedparser.parse(request.POST.get('url'))

    parsed = FeedParser.parse(feed_data)
    _entries = parsed.pop('entries')

    try:
        feed = Feed.objects.create(**parsed)
    except IntegrityError:
        feed = Feed.objects.get(href=parsed['href'])

    feed.users.add(request.user)

    serializer = FeedHyperlinkedModelSerializer(feed, context={'request': request})

    for _entry in _entries:
        entry_parsed = EntryParser.parse(_entry)
        entry_parsed.update({'feed': serializer.data['url']})

        _entry_serializer = EntryHyperlinkedModelSerializer(data=entry_parsed)
        _entry_serializer.is_valid(raise_exception=True)
        _entry_serializer.save()

    return redirect('feeds')
