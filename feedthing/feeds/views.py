from django.shortcuts import render

import feedparser


def add_feed(request):
    context = {}

    if request.method == 'POST':
        url = request.POST.get('url')
        feed = feedparser.parse(url)

        context = {
            'root_keys': feed.keys(),
            'feed_keys': feed['feed'].keys()
        }

    return render(request, 'index.html', context=context)
