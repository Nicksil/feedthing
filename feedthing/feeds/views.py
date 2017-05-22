from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render

from api.endpoints.entry_details import EntryDetailsEndpoint
from api.endpoints.feed_details import FeedDetailsEndpoint
from api.endpoints.feed_index import FeedIndexEndpoint
from core.exceptions import FeedManagerError


@login_required
def index(request):
    return render(request, 'feeds/index.html', {
        'feeds': FeedIndexEndpoint.as_view()(request).data
    })


@login_required
def add_feed(request):
    try:
        FeedIndexEndpoint.as_view()(request)
    except IntegrityError:
        messages.info(request, 'Feed already exists.')
    except ValidationError as e:
        for msg in e.messages:
            messages.info(request, msg)
    except FeedManagerError as e:
        messages.info(request, e)

    return redirect('feeds:index')


@login_required
def detail(request, feed_uid):
    return render(request, 'feeds/detail.html', {
        'feed': FeedDetailsEndpoint.as_view()(request, feed_uid=feed_uid).data
    })


@login_required
def fetch(request, feed_uid):
    request.method = 'POST'
    FeedDetailsEndpoint.as_view()(request, feed_uid=feed_uid)
    return redirect('feeds:detail', feed_uid)


@login_required
def delete(request, feed_uid):
    request.method = 'DELETE'
    FeedDetailsEndpoint.as_view()(request, feed_uid=feed_uid)
    return redirect('feeds:index')


@login_required
def edit(request, feed_uid):
    if request.method == 'POST':
        request.method = 'PATCH'
        FeedDetailsEndpoint.as_view()(request, feed_uid=feed_uid)
        return redirect('feeds:detail', feed_uid)
    return render(request, 'feeds/edit.html', {
        'feed': FeedDetailsEndpoint.as_view()(request, feed_uid=feed_uid).data
    })


@login_required
def entry(request, feed_uid, entry_uid):
    return render(request, 'feeds/entry.html', {
        'entry': EntryDetailsEndpoint.as_view()(
            request,
            feed_uid=feed_uid,
            entry_uid=entry_uid
        ).data
    })
