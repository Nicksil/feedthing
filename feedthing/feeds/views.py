from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render

from bs4 import BeautifulSoup

from .models import Entry
from .models import Feed
from api.endpoints.feed_index import FeedIndexEndpoint


def index(request):
    if request.method == 'POST':
        return add_feed(request)

    feeds = FeedIndexEndpoint.as_view()(request).data

    return render(request, 'feeds/index.html', {'feeds': feeds})


@login_required
def add_feed(request):
    FeedIndexEndpoint.as_view()(request)
    return redirect('feeds:index')


@login_required
def mark_read(request):
    entries = request.POST.getlist('entries')
    Entry.objects.filter(
        uid__in=entries,
        feed__user=request.user
    ).update(read=True)

    return redirect('feeds:index')


@login_required
def import_opml(request):
    opml_file = request.FILES.get('opml_file')
    soup = BeautifulSoup(opml_file.read(), 'xml')
    opml_file.close()
    urls = [u['xmlUrl'] for u in soup.find_all('outline', type='rss')]

    for url in urls:
        try:
            Feed.objects.create(href=url, user=request.user)
        except IntegrityError:
            pass

    return redirect('feeds:index')
