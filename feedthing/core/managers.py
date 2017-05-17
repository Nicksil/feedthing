from typing import List
from typing import Optional
from typing import Union
import datetime
import logging

from django.conf import settings

import feedparser

from .descriptors import DateTime
from .descriptors import String
from .descriptors import URL
from .descriptors import User
from .utils import now
from .utils import struct_time_to_datetime
from feeds.models import Feed

logger = logging.getLogger(__name__)


class FeedManager:
    etag = String('etag', default='')
    href = URL('href')
    html_href = URL('html_href', default='')
    last_fetch = DateTime('last_fetch')
    title = String('title', default='<NO_TITLE>')
    user = User('user')

    def __init__(self, feed=None, href=None, user=None):
        # We must have an href value if we're going to query an API
        # We can ascertain a href value from either a Feed object or
        # href parameter.
        if not feed and not href:
            raise ValueError('Must provide a Feed object or an href value.')

        self.data = None
        self.feed = feed

    # @property
    # def etag(self):
    #     if self.data and 'etag' in self.data:
    #         return self.data.etag
    #
    #     if self.feed:
    #         return self.feed.etag
    #
    #     return ''

    # @property
    # def href(self):
    #     # Fresh data will have most up-to-date
    #     if self.data and 'href' in self.data:
    #         return self.data['href']
    #
    #     # Check if user supplied
    #     if self._href:
    #         return self._href
    #
    #     # If we're here, there must be a Feed object
    #     return self.feed.href

    # @property
    # def html_href(self):
    #     if self.data:
    #         links = self.data['feed'].get('links', [])
    #         for link in links:
    #             if link['rel'] == 'alternate' and link['type'] == 'text/html':
    #                 return link['href']
    #
    #     if self.feed and self.feed.html_href:
    #         return self.feed.html_href

        # There's not always going to be and html href w/in a feedparser payload.
        # And we don't need the value to complete any work.
        # Don't want to raise an exception right now, just return an empty string
        # return ''

    # @property
    # def last_fetch(self):
    #     if self.data:
    #         return now()
    #
    #     if self.feed:
    #         return self.feed.last_fetch
    #
    #     return None

    # @property
    # def title(self):
    #     if self.data and 'feed' in self.data and 'title' in self.data.feed:
    #         return self.data.feed.title
    #
    #     if self.feed:
    #         return self.feed.title
    #
    #     return '<NO_TITLE>'

    # @property
    # def user(self):
    #     if self._user:
    #         return self._user
    #     if self.feed:
    #         return self.feed.user
    #     return None

    def build_request_kwargs(self):
        kwargs = {'agent': settings.USER_AGENT_STR}

        if self.feed:
            if self.feed.etag:
                kwargs['etag'] = self.feed.etag
            elif self.feed.last_modified:
                kwargs['modified'] = self.feed.last_modified.isoformat()

        return kwargs

    def create(self):
        assert self.user is not None, 'Must have a User object to create a new Feed record.'

        kwargs = self.build_request_kwargs()
        self.data = self.fetch_source(**kwargs)
        return Feed.objects.create(**self.to_internal())

    def fetch_source(self, **kwargs):
        return feedparser.parse(self.href, **kwargs)

    def to_internal(self):
        return {
            # 'entries': self.entries,
            'etag': self.etag,
            'href': self.href,
            'html_href': self.html_href,
            'last_fetch': self.last_fetch,
            'title': self.title,
            'user': self.user
        }


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
