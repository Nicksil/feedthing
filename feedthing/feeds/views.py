from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .models import Feed
from api.endpoints.entry_details import EntryDetailsEndpoint
from api.endpoints.feed_details import FeedDetailsEndpoint
from api.endpoints.feed_index import FeedIndexEndpoint


@login_required
def index(request):
    feeds = []
    for feed in request.user.feeds.all().order_by('title'):
        feeds.append({
            'title': feed.title,
            'id': feed.id,
            'updated': feed.updated
        })
    return render(request, 'feeds/index.html', {'feeds': feeds})


@login_required
def add_feed(request):
    response = FeedIndexEndpoint.as_view()(request)
    if 'error' in response.data:
        messages.info(request, response.data['error'])
    return redirect('feeds:index')


@login_required
def detail(request, feed_id):
    feed_obj = Feed.objects.get(id=feed_id)
    entry_objs = feed_obj.entries.all()
    entries = []

    for entry in entry_objs:
        if entry.summary_string:
            summary = entry.summary_string
        else:
            summary = entry.content_string

        entries.append({
            'id': entry.id,
            'published': entry.published,
            'summary': summary,
            'title': entry.title,
        })

    feed = {
        'entries': entries,
        'id': feed_obj.id,
        'title': feed_obj.title,
    }

    return render(request, 'feeds/detail.html', {'feed': feed})


@login_required
def fetch(request, feed_id):
    request.method = 'POST'
    FeedDetailsEndpoint.as_view()(request, feed_id=feed_id)
    return redirect('feeds:detail', feed_id)


@login_required
def delete(request, feed_id):
    request.method = 'DELETE'
    FeedDetailsEndpoint.as_view()(request, feed_id=feed_id)
    return redirect('feeds:index')


@login_required
def edit(request, feed_id):
    if request.method == 'POST':
        request.method = 'PATCH'
        FeedDetailsEndpoint.as_view()(request, feed_id=feed_id)
        return redirect('feeds:detail', feed_id)
    return render(request, 'feeds/edit.html', {
        'feed': FeedDetailsEndpoint.as_view()(request, feed_id=feed_id).data
    })


@login_required
def entry_detail(request, feed_id, entry_id):
    data = EntryDetailsEndpoint.as_view()(
        request,
        feed_id=feed_id,
        entry_id=entry_id
    ).data
    data.update({'feed': reverse('feeds:detail', kwargs={'feed_id': feed_id})})
    return render(request, 'feeds/entry.html', {'entry': data})
