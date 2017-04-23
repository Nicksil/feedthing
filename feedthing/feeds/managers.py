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

    @classmethod
    def fetch_and_save(cls, user, feed=None, href=None):
        _instance = cls(user, feed=feed, href=href)
        _fetched = _instance.fetch()
        _prepped = _instance.prepare(_fetched)

        return _instance.save(_prepped)


class FeedEntryManager:
    """A very simple, cursory implementation to handle Entry model objects.
    """

    def __init__(self, feed):
        self.feed = feed

    def fetch(self):
        parsed = feedparser.parse(self.feed.href)
        return parsed.get('entries', [])

    def prepare(self, entry):
        _link = self.get_link(entry)
        _published = entry.get('published_parsed', None)

        if _published and isinstance(_published, time.struct_time):
            _published = ensure_aware(self.convert_struct_time(_published))

        return {
            'feed': self.feed,
            'link': _link,
            'published': _published,
            'title': entry.get('title', ''),
        }

    @staticmethod
    def get_link(entry):
        if 'feedburner_origlink' in entry:
            return entry['feedburner_origlink']

        return entry.get('link', '')

    @staticmethod
    def convert_struct_time(value):
        """Converts a time.struct_time object to a datetime.datetime object
        """
        return datetime.datetime.fromtimestamp(time.mktime(value))

    @staticmethod
    def save(data):
        try:
            return Entry.objects.create(**data)
        except IntegrityError:
            return None

    @classmethod
    def fetch_and_save(cls, feed):
        _instance = cls(feed)
        entries = _instance.fetch()
        parsed = [_instance.prepare(e) for e in entries]

        return [_instance.save(p) for p in parsed]
