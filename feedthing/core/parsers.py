from typing import Optional
import datetime
import time

import feedparser

from .utils import ensure_aware


class BaseParser:
    def __init__(self, data: feedparser.FeedParserDict) -> None:
        self.data = data

    @classmethod
    def parse(cls, data: feedparser.FeedParserDict) -> dict:
        _instance = cls(data)
        return _instance._parse()

    def _parse(self) -> dict:
        return {}

    def _get_href(self) -> str:
        raise NotImplementedError


class FeedParser(BaseParser):
    def _parse(self) -> dict:
        return {
            'entries': self.data.get('entries', []),
            'etag': self.data.get('etag', ''),
            'last_modified': self._get_last_modified(),
            'title': self._get_title(),
        }

    def _get_href(self) -> str:
        links = self.data['feed'].get('links', [])
        # FIXME: If this link is diff from href used, re-run fetch to get true feed
        for link in links:
            if link['type'] == 'application/rss+xml':
                return link['href']

        return self.data['href']

    def _get_last_modified(self) -> Optional[datetime.datetime]:
        last_modified = self.data.get('modified_parsed', None)
        if last_modified:
            return ensure_aware(
                datetime.datetime.fromtimestamp(time.mktime(last_modified))
            )

    def _get_title(self) -> str:
        feed = self.data.get('feed')

        if feed and 'title' in feed:
            return feed['title']

        return ''


class EntryParser(BaseParser):
    def _parse(self) -> dict:
        return {
            'href': self._get_href(),
            'published': self._get_published(),
            'title': self.data.get('title', ''),
        }

    def _get_href(self) -> str:
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
