"""
users.managers
~~~~~~~~~~~~~~
"""

import datetime
import time

from django.db import IntegrityError

import feedparser

from .models import Entry
from .models import Feed
from core.utils import ensure_aware


class FeedManager:
    """A very simple, cursory implementation to handle Feed model objects.
    """

    def __init__(self, user, feed=None, href=None):
        self.entries = []
        self.feed = feed
        self.href = href
        self.user = user

    def fetch(self):
        _url = None

        if self.feed is not None and self.feed.href:
            _url = self.feed.href
        elif self.href is not None:
            _url = self.href

        if not _url:
            raise RuntimeError('No URL to fetch the feed.')

        return feedparser.parse(_url)

    def prepare(self, data):
        self.entries = data.get('entries', [])

        _etag = data.get('etag', '')
        _feed = data.get('feed')
        _headers = data.get('headers')
        _href = data.get('href', '')

        if _headers and 'Last-Modified' in _headers:
            _last_modified = _headers['Last-Modified']
        else:
            _last_modified = ''

        if _feed and 'title' in _feed:
            _title = _feed['title']
        else:
            _title = ''

        return {
            'etag': _etag,
            'href': _href,
            'last_modified': _last_modified,
            'title': _title,
            'user': self.user,
        }

    @staticmethod
    def save(data):
        return Feed.objects.create(**data)


class FeedEntryManager:
    """A very simple, cursory implementation to handle Entry model objects.
    """

    def __init__(self, feed=None, feed_id=None):
        if feed is not None and feed_id is not None:
            raise RuntimeError('Cannot provide both feed and feed_id arguments.')

        if feed_id:
            self.feed = Feed.objects.get(pk=feed_id)
        else:
            self.feed = feed

    def fetch(self):
        parsed = feedparser.parse(self.feed.href)
        return parsed.get('entries', [])

    def prepare(self, data):
        if 'feedburner_origlink' in data:
            _link = data['feedburner_origlink']
        else:
            _link = data.get('link', '')

        _published = data.get('published_parsed', None)

        if _published and isinstance(_published, time.struct_time):
            _published = ensure_aware(datetime.datetime.fromtimestamp(time.mktime(_published)))

        return {
            'feed': self.feed,
            'link': _link,
            'published': _published,
            'title': data.get('title', ''),
        }

    @staticmethod
    def save(data):
        try:
            return Entry.objects.create(**data)
        except IntegrityError:
            return None

    @classmethod
    def fetch_and_save(cls, feed=None, feed_id=None):
        _instance = cls(feed=feed, feed_id=feed_id)
        entries = _instance.fetch()
        parsed = [_instance.prepare(e) for e in entries]

        return [_instance.save(p) for p in parsed]
