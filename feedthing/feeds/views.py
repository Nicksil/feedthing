from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from api.endpoints.entry_details import EntryDetailsEndpoint
from api.endpoints.feed_details import FeedDetailsEndpoint
from api.endpoints.feed_index import FeedIndexEndpoint


@login_required
def index(request):
    return render(request, 'feeds/index.html', {
        'feeds': FeedIndexEndpoint.as_view()(request).data
    })


@login_required
def add_feed(request):
    response = FeedIndexEndpoint.as_view()(request)
    if 'error' in response.data:
        messages.info(request, response.data['error'])
    return redirect('feeds:index')


@login_required
def detail(request, feed_id):
    return render(request, 'feeds/detail.html', {
        'feed': FeedDetailsEndpoint.as_view()(request, feed_id=feed_id).data
    })


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
def entry(request, feed_id, entry_id):
    data = EntryDetailsEndpoint.as_view()(
        request,
        feed_id=feed_id,
        entry_id=entry_id
    ).data
    data.update({'feed': reverse('feeds:detail', kwargs={'feed_id': feed_id})})
    return render(request, 'feeds/entry.html', {'entry': data})
