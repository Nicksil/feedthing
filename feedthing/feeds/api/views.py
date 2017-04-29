import time

import datetime
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
import feedparser

from core.utils import ensure_aware
from ..models import Feed
from .serializers import FeedHyperlinkedModelSerializer


class FeedAPIViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedHyperlinkedModelSerializer

    def create(self, request, *args, **kwargs):
        feed_data = feedparser.parse(request.data['href'])

        etag = feed_data.get('etag', '')
        href = feed_data.get('href', '')

        _entries = feed_data.get('entries', [])
        _feed = feed_data.get('feed')
        _headers = feed_data.get('headers')

        if _headers and 'Last-Modified' in _headers:
            last_modified = _headers['Last-Modified']
        else:
            last_modified = ''

        if _feed and 'title' in _feed:
            title = _feed['title']
        else:
            title = ''

        request.data.update({
            'etag': etag,
            'href': href,
            'last_modified': last_modified,
            'title': title,
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        for _entry in _entries:
            if 'feedburner_origlink' in _entry:
                link = _entry['feedburner_origlink']
            else:
                link = _entry.get('link', '')

            _published = _entry.get('published_parsed', None)
            if _published and isinstance(_published, time.struct_time):
                _published = ensure_aware(datetime.datetime.fromtimestamp(time.mktime(_published)))

            title = _entry.get('title', '')

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
