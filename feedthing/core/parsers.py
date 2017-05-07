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
