from typing import List
from typing import Optional
from typing import Type
from typing import Union
import datetime

from django.contrib.auth.base_user import AbstractBaseUser

import feedparser

from .utils import struct_time_to_datetime
from feeds.models import Feed


class FeedDataManager:
    def __init__(self,
                 href: Optional[str] = None,
                 feed: Optional[Feed] = None,
                 user: Type[AbstractBaseUser] = None
                 ) -> None:
        self.data = feedparser.FeedParserDict()
        self.feed = feed
        self.href = href
        self.user = user

    @property
    def entries(self) -> list:
        if self.data and self.data.entries:
            return EntryDataManager.parse(self.data.entries, self.feed, many=True)
        return []

    @classmethod
    def fetch(cls,
              href: str,
              feed: Optional[Feed] = None,
              user: Type[AbstractBaseUser] = None
              ) -> dict:
        mgr = cls(href, feed=feed, user=user)
        mgr.fetch_data()
        return mgr.to_internal()

    def fetch_data(self) -> feedparser.FeedParserDict:
        kwargs = {}

        if self.feed:
            if self.feed.etag:
                kwargs['etag'] = self.feed.etag
            elif self.feed.last_modified:
                kwargs['modified'] = str(self.feed.last_modified)

        self.data = feedparser.parse(self._href)

        return self.data

    def to_internal(self, data: Optional[feedparser.FeedParserDict] = None) -> dict:
        if data is None:
            data = self.data

        return {
            'etag': data.get('etag', ''),
            'href': self._href,
            'last_modified': self._get_last_modified(data),
            'title': data['feed'].get('title', ''),
            'user': self.user
        }

    def _get_last_modified(self, data: Optional[feedparser.FeedParserDict] = None) -> Optional[datetime.datetime]:
        if data is None:
            data = self.data

        last_modified = data.get('modified_parsed', None)

        if last_modified is not None:
            return struct_time_to_datetime(last_modified)

        return None

    @property
    def _href(self):
        if self.href:
            return self.href

        if self.feed and self.feed.href:
            return self.feed.href

        if not self.href and not self.feed:
            raise RuntimeError(
                'Must provide either a valid ``href<str>`` or'
                '``feed<Feed>`` with valid href attribute.'
            )


class EntryDataManager:
    def __init__(self, data: feedparser.FeedParserDict, feed: Optional[Feed] = None) -> None:
        self.data = data
        self.feed = feed

    def to_internal(self) -> dict:
        return {
            'feed': self.feed,
            'href': self._get_href(),
            'published': self._get_published(),
            'title': self.data.get('title', '')
        }

    @classmethod
    def parse(cls,
              data: Union[feedparser.FeedParserDict, List[feedparser.FeedParserDict]],
              feed: Optional[Feed] = None,
              many: bool = False
              ) -> Union[dict, List[dict]]:
        if many:
            if not isinstance(data, list):
                raise TypeError('data should be a list if many == True.')

            entries = []

            for entry in data:
                entries.append(cls.parse(entry, feed=feed, many=False))

            return entries

        instance = cls(data, feed=feed)
        return instance.to_internal()

    def _get_href(self) -> str:
        if 'feedburner_origlink' in self.data:
            return self.data['feedburner_origlink']

        return self.data.get('link', '')

    def _get_published(self) -> Optional[datetime.datetime]:
        published = self.data.get('published_parsed', None)

        if published is not None:
            return struct_time_to_datetime(published)

        return None
