import datetime
import time

from django.db import IntegrityError

import feedparser

from .models import Entry
from core.utils import ensure_aware


class FeedEntryManager:
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
        """Converts a time.struct_time object to a datetime.datetime object"""
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
