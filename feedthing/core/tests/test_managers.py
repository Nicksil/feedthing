from unittest import mock
import datetime
import os
import time

from django.conf import settings
from django.test import TestCase

import feedparser

from ..managers import EntryDataManager
from ..managers import FeedManager
from feeds.tests.factories import FeedFactory


def get_feedparser_parsed():
    data_path = os.path.join(settings.PROJECT_DIR, 'core/tests/data/feed.xml')

    with open(data_path) as feedfile:
        data = feedfile.read()

    return feedparser.parse(data)


class CoreManagersTestCase(TestCase):
    def setUp(self):
        self.feedparserdict = get_feedparser_parsed()

    @mock.patch.object(feedparser, 'parse')
    def test_FeedDataManager_fetch_data_returns_FeedParserDict(self, parse):
        parse.return_value = self.feedparserdict

        mgr = FeedManager(href='https://example.com')
        result = mgr.fetch_data()

        self.assertIsInstance(result, feedparser.FeedParserDict)

    @mock.patch.object(feedparser, 'parse')
    def test_FeedDataManager_to_internal_returns_dict(self, parse):
        parse.return_value = self.feedparserdict

        mgr = FeedManager(href='https://example.com')
        data = mgr.fetch_data()
        result = mgr.to_internal(data)

        self.assertIsInstance(result, dict)

    @mock.patch.object(feedparser, 'parse')
    def test_FeedDataManager_fetch_classmethod_returns_dict(self, parse):
        parse.return_value = self.feedparserdict

        result = FeedManager.fetch(href='https://example.com')

        self.assertIsInstance(result, dict)

    def test_FeedDataManager_get_last_modified_returns_datetime_object(self):
        fake = feedparser.FeedParserDict()
        fake['modified_parsed'] = time.localtime()

        mgr = FeedManager()
        result = mgr._get_last_modified(fake)

        self.assertIsInstance(result, datetime.datetime)

    def test_FeedDataManager_get_last_modified_returns_None_when_key_does_not_exist(self):
        mgr = FeedManager()
        result = mgr._get_last_modified()

        self.assertIsNone(result)

    def test_FeedDataManager_href_property_raises_RuntimeError_when_no_href_or_feed_object_given(self):
        mgr = FeedManager()

        with self.assertRaises(RuntimeError):
            # noinspection PyStatementEffect
            mgr._href

    def test_FeedDataManager_href_property_returns_correct_value_when_href_given_at_init(self):
        fake_href = 'https://example.com'
        mgr = FeedManager(href=fake_href)

        self.assertEqual(mgr._href, fake_href)

    def test_FeedDataManager_href_property_returns_correct_value_when_feed_object_given_at_init(self):
        fake_feed = FeedFactory()
        mgr = FeedManager(feed=fake_feed)

        self.assertEqual(mgr._href, fake_feed.href)

    def test_FeedDataManager_href_property_returns_correct_value_when_both_href_and_feed_object_given(self):
        fake_feed = FeedFactory()
        fake_href = 'https://example.com'
        mgr = FeedManager(feed=fake_feed, href=fake_href)

        self.assertEqual(mgr._href, fake_href)

    @mock.patch.object(feedparser, 'parse')
    def test_FeedDataManager_entries_property_call_returns_list(self, parse):
        parse.return_value = self.feedparserdict

        mgr = FeedManager(href='https://example.com')
        mgr.fetch_data()
        result = mgr.entries

        self.assertIsInstance(result, list)

    def test_FeedDataManager_entries_property_call_returns_empty_list(self):
        mgr = FeedManager()
        result = mgr.entries

        self.assertEqual(len(result), 0)

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

    @mock.patch.object(feedparser, 'parse')
    def test_EntryDataManager_parse_classmethod_raise_TypeError_when_called_with_many_is_True_and_passing_in_single_item(self, parse):
        parse.return_value = self.feedparserdict

        feed_mgr = FeedManager(href='https://example.com')
        feed_mgr.fetch_data()

        with self.assertRaises(TypeError):
            EntryDataManager.parse(feed_mgr.entries[0], many=True)
