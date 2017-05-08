from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from api.endpoints.feed_index import FeedIndexEndpoint


def index(request):
    if request.method == 'POST':
        return add_feed(request)
    feeds = FeedIndexEndpoint.as_view()(request).data
    return render(request, 'index.html', {'feeds': feeds})


@login_required
def add_feed(request):
    FeedIndexEndpoint.as_view()(request)
    return redirect('index')
