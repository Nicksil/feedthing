from typing import List
from typing import Optional
from typing import Type
from typing import Union
import datetime
import logging

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser

import feedparser

from .utils import now
from .utils import struct_time_to_datetime
from feeds.models import Feed

logger = logging.getLogger(__name__)


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
              href: Optional[str] = None,
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
            else:
                logger.debug('No etag, last_modified values for {}'.format(repr(self.feed)))

        logger.debug('Sending request to {}'.format(self._href))
        self.data = feedparser.parse(self._href, agent=settings.USER_AGENT_STR)

        if 'status' in self.data:
            logger.debug('feedparser returns with status {}'.format(self.data.status))

        return self.data

    def to_internal(self, data: Optional[feedparser.FeedParserDict] = None) -> dict:
        if data is None:
            data = self.data

        return {
            'etag': data.get('etag', ''),
            'href': self._href,
            'html_href': self._get_html_href(data),
            'last_fetch': now(),
            'last_modified': self._get_last_modified(data),
            'title': data['feed'].get('title', 'NO TITLE'),
            'user': self.user
        }

    def _get_html_href(self, data: Optional[feedparser.FeedParserDict] = None) -> str:
        if data is None:
            data = self.data

        links = data['feed'].get('links', [])

        for link in links:
            if link['rel'] == 'alternate' and link['type'] == 'text/html':
                return link['href']

        return ''

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
            'title': self.data.get('title', 'NO TITLE')
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
        published = None

        if 'published_parsed' in self.data:
            published = self.data['published_parsed']
        elif 'updated_parsed' in self.data:
            published = self.data['updated_parsed']

        if published is not None:
            published = struct_time_to_datetime(published)

        return published
