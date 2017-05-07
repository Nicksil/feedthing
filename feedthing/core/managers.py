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
    def __init__(self, href: str, user: Type[AbstractBaseUser] = None) -> None:
        self.data = feedparser.FeedParserDict()
        self.href = href
        self.user = user

    @classmethod
    def fetch(cls, href: str, user: Type[AbstractBaseUser] = None) -> dict:
        mgr = cls(href, user=user)
        mgr.fetch_data()

        return mgr.to_internal()

    def fetch_data(self) -> feedparser.FeedParserDict:
        self.data = feedparser.parse(self.href)
        return self.data

    def to_internal(self) -> dict:
        return {
            'etag': self.data.get('etag', ''),
            'href': self.href,
            'last_modified': self._get_last_modified(),
            'title': self.data['feed'].get('title', ''),
            'user': self.user
        }

    def _get_last_modified(self) -> Optional[datetime.datetime]:
        last_modified = self.data.get('modified_parsed', None)

        if last_modified is not None:
            return struct_time_to_datetime(last_modified)

        return None


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
