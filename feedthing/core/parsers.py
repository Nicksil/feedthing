from typing import Optional
import datetime
import time

import feedparser

from .utils import ensure_aware


class FeedParser:
    def __init__(self, data: feedparser.FeedParserDict):
        self.data = data

    @classmethod
    def parse(cls, data: feedparser.FeedParserDict) -> dict:
        _instance = cls(data)
        return _instance._parse()

    def _parse(self) -> dict:
        return {
            'entries': self.data.get('entries', []),
            'etag': self.data.get('etag', ''),
            'href': self.data.get('href', ''),
            'last_modified': self._get_last_modified(),
            'title': self._get_title(),
        }

    def _get_last_modified(self) -> str:
        headers = self.data.get('headers')

        if headers and 'Last-Modified' in headers:
            return headers['Last-Modified']

        return ''

    def _get_title(self) -> str:
        feed = self.data.get('feed')

        if feed and 'title' in feed:
            return feed['title']

        return ''


class EntryParser:
    def __init__(self, data: feedparser.FeedParserDict):
        self.data = data

    @classmethod
    def parse(cls, data: feedparser.FeedParserDict) -> dict:
        _instance = cls(data)
        return _instance._parse()

    def _parse(self):
        link = self._get_link()
        published = self._get_published()

        return {
            'href': link,
            'published': published,
            'title': self.data.get('title', ''),
        }

    def _get_link(self) -> str:
        if 'feedburner_origlink' in self.data:
            return self.data['feedburner_origlink']

        return self.data.get('link', '')

    def _get_published(self) -> Optional[datetime.datetime]:
        published = self.data.get('published_parsed', None)

        if published:
            published = ensure_aware(
                datetime.datetime.fromtimestamp(time.mktime(published))
            )

        return published
