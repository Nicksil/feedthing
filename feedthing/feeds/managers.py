import datetime
import time

import feedparser

from feeds.models import Entry


class FeedEntryManager:
    def __init__(self, feed):
        self.feed = feed

    def fetch(self):
        parsed = feedparser.parse(self.feed.href)
        return parsed.get('entries', [])

    def prepare(self, entry):
        _published = entry.get('published_parsed', None)

        if _published and isinstance(_published, time.struct_time):
            _published = self.convert_struct_time(_published)

        return {
            'feed': self.feed,
            'link': entry.get('link', ''),
            'published': _published,
            'title': entry.get('title', ''),
        }

    def convert_struct_time(self, value):
        """Converts a time.struct_time object to a datetime.datetime object"""
        return datetime.datetime(time.mktime(value))

    @staticmethod
    def save(data):
        return Entry.objects.create(**data)

    @classmethod
    def fetch_and_save(cls, feed):
        _instance = cls(feed)
        entries = _instance.fetch()
        parsed = [_instance.prepare(e) for e in entries]
        # ------------- PDEBUG -------------
        print('=' * 100)
        print(parsed)
        print('=' * 100)
        # ------------- PDEBUG -------------
        return [_instance.save(p) for p in parsed]
