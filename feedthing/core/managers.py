from typing import List
from typing import Optional
from typing import Union
import datetime
import logging

from django.conf import settings

import feedparser

from .utils import now
from .utils import struct_time_to_datetime
from feeds.models import Feed

logger = logging.getLogger(__name__)


class FeedManager:
    def __init__(self, feed=None, href=None):
        self._href = href
        self.data = None
        self.feed = feed

    @property
    def entries(self):
        if self.data and 'entries' in self.data:
            return EntryDataManager.parse(self.data.entries, self.feed, many=True)
        return []

    @property
    def href(self):
        # Fresh data will have most up-to-date
        if self.data and 'href' in self.data:
            return self.data['href']

        # Check if user supplied
        if self._href:
            return self._href

        # Try the Feed if given
        if self.feed and self.feed.href:
            return self.feed.href

        # Finally, there's no way to ascertain an href value.
        raise ValueError('Could not ascertain href.')

    @property
    def html_href(self):
        if self.data:
            links = self.data['feed'].get('links', [])
            for link in links:
                if link['rel'] == 'alternate' and link['type'] == 'text/html':
                    return link['href']

        if self.feed and self.feed.html_href:
            return self.feed.html_href

        # There's not always going to be and html href w/in a feedparser payload.
        # And we don't need the value to complete any work.
        # Don't want to raise an exception right now, just return an empty string
        return ''

    @property
    def title(self):
        if self.data and 'feed' in self.data and 'title' in self.data.feed:
            return self.data.feed.title

        if self.feed:
            return self.feed.title

        return '<NO_TITLE>'

    def create(self):
        kwargs = self.build_request_kwargs()
        self.data = self.fetch_source(**kwargs)

    def build_request_kwargs(self):
        kwargs = {'agent': settings.USER_AGENT_STR}

        if self.feed:
            if self.feed.etag:
                kwargs['etag'] = self.feed.etag
            elif self.feed.last_modified:
                kwargs['modified'] = self.feed.last_modified.isoformat()

        return kwargs

    def fetch_source(self, **kwargs):
        return feedparser.parse(self.href, **kwargs)

    def to_internal(self, data):
        return {
            'entries': self.entries,
            'etag': data.get('etag', ''),
            'href': self.href,
            'html_href': self.html_href,
            'last_fetch': now(),
            'title': self.title,
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
