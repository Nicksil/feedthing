import datetime
import os

from django.conf import settings
from django.test import TestCase

import feedparser

from ..managers import EntryDataManager


def get_feedparser_parsed():
    data_path = os.path.join(settings.PROJECT_DIR, 'core/tests/data/feed.xml')

    with open(data_path) as feedfile:
        data = feedfile.read()

    return feedparser.parse(data)


class CoreManagersTestCase(TestCase):
    def setUp(self):
        self.feedparserdict = get_feedparser_parsed()

    def test_EntryDataManager_to_internal_returns_dict(self):
        feed_data = get_feedparser_parsed()
        mgr = EntryDataManager(feed_data.entries[0])
        result = mgr.to_internal()

        self.assertIsInstance(result, dict)

    def test_EntryDataManager_get_href_returns_str(self):
        feed_data = get_feedparser_parsed()
        mgr = EntryDataManager(feed_data.entries[0])
        result = mgr._get_href()

        self.assertIsInstance(result, str)

    def test_EntryDataManager_get_href_without_feedburner_link_returns_str(self):
        feed_data = get_feedparser_parsed()
        entry = feed_data.entries[0]
        entry.pop('feedburner_origlink', None)
        mgr = EntryDataManager(entry)
        result = mgr._get_href()

        self.assertIsInstance(result, str)

    def test_EntryDataManager_get_published_returns_datetime_object(self):
        feed_data = get_feedparser_parsed()
        mgr = EntryDataManager(feed_data.entries[0])
        result = mgr._get_published()

        self.assertIsInstance(result, datetime.datetime)

    def test_EntryDataManager_get_published_returns_None(self):
        feed_data = get_feedparser_parsed()
        entry = feed_data.entries[0]
        entry.pop('published_parsed', None)
        mgr = EntryDataManager(entry)
        result = mgr._get_published()

        self.assertIsNone(result)
