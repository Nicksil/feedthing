from unittest import mock
import os
import time

import datetime
from django.conf import settings
from django.test import TestCase

import feedparser

from feeds.tests.factories import FeedFactory
from ..managers import FeedDataManager


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

        mgr = FeedDataManager(href='https://example.com')
        result = mgr.fetch_data()

        self.assertIsInstance(result, feedparser.FeedParserDict)

    @mock.patch.object(feedparser, 'parse')
    def test_FeedDataManager_to_internal_returns_dict(self, parse):
        parse.return_value = self.feedparserdict

        mgr = FeedDataManager(href='https://example.com')
        data = mgr.fetch_data()
        result = mgr.to_internal(data)

        self.assertIsInstance(result, dict)

    def test_FeedDataManager_get_last_modified_returns_datetime_object(self):
        fake = feedparser.FeedParserDict()
        fake['modified_parsed'] = time.localtime()

        mgr = FeedDataManager()
        result = mgr._get_last_modified(fake)

        self.assertIsInstance(result, datetime.datetime)

    def test_FeedDataManager_get_last_modified_returns_None_when_key_does_not_exist(self):
        mgr = FeedDataManager()
        result = mgr._get_last_modified()

        self.assertIsNone(result)

    def test_FeedDataManager_href_property_raises_RuntimeError_when_no_href_or_feed_object_given(self):
        mgr = FeedDataManager()

        with self.assertRaises(RuntimeError):
            # noinspection PyStatementEffect
            mgr._href

    def test_FeedDataManager_href_property_returns_correct_value_when_href_given_at_init(self):
        fake_href = 'https://example.com'
        mgr = FeedDataManager(href=fake_href)

        self.assertEqual(mgr._href, fake_href)

    def test_FeedDataManager_href_property_returns_correct_value_when_feed_object_given_at_init(self):
        fake_feed = FeedFactory()
        mgr = FeedDataManager(feed=fake_feed)

        self.assertEqual(mgr._href, fake_feed.href)

    def test_FeedDataManager_href_property_returns_correct_value_when_both_href_and_feed_object_given(self):
        fake_feed = FeedFactory()
        fake_href = 'https://example.com'
        mgr = FeedDataManager(feed=fake_feed, href=fake_href)

        self.assertEqual(mgr._href, fake_href)
