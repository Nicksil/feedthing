import datetime
import time

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

import feedparser

from ..models import Feed
from .serializers import FeedHyperlinkedModelSerializer
from core.parsers import FeedParser
from core.utils import ensure_aware
from entries.api.serializers import EntryHyperlinkedModelSerializer


class FeedAPIViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedHyperlinkedModelSerializer

    def create(self, request, *args, **kwargs):
        feed_data = feedparser.parse(request.data['href'])

        parsed = FeedParser.parse(feed_data)
        _entries = parsed.pop('entries')
        request.data.update(parsed)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feed = serializer.save()
        feed.users.add(request.user)

        for _entry in _entries:
            entry_parsed = self.parse_entry_response(_entry)
            entry_parsed.update({'feed': serializer.data['url']})

            _entry_serializer = EntryHyperlinkedModelSerializer(data=entry_parsed)
            _entry_serializer.is_valid(raise_exception=True)
            _entry_serializer.save()

        serializer = self.get_serializer(feed)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def parse_entry_response(entry: feedparser.FeedParserDict) -> dict:
        if 'feedburner_origlink' in entry:
            link = entry['feedburner_origlink']
        else:
            link = entry.get('link', '')

        _published = entry.get('published_parsed', None)
        if _published and isinstance(_published, time.struct_time):
            _published = ensure_aware(datetime.datetime.fromtimestamp(time.mktime(_published)))

        return {
            'href': link,
            'published': _published,
            'title': entry.get('title', ''),
        }
