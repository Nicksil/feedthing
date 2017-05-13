from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from api.endpoints.feed_details import FeedDetailsEndpoint
from api.endpoints.feed_index import FeedIndexEndpoint


@login_required
def index(request):
    if request.method == 'POST':
        return add_feed(request)
    return render(request, 'feeds/index.html', {
        'feeds': FeedIndexEndpoint.as_view()(request).data
    })


@login_required
def add_feed(request):
    FeedIndexEndpoint.as_view()(request)
    return redirect('feeds:index')


@login_required
def detail(request, feed_uid):
    return render(request, 'feeds/detail.html', {
        'feed': FeedDetailsEndpoint.as_view()(request, feed_uid=feed_uid).data
    })
