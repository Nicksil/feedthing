import json
import os
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

import feedparser

from feeds.managers import FeedManager
from feeds.models import Feed
from feeds.tests.factories import FeedFactory
from users.tests.factories import UserFactory


class FeedEndpointsTests(TestCase):
    def setUp(self):
        self.simple_user_pw = 'simple_password'
        self.simple_user = UserFactory(password=self.simple_user_pw)

    def test_feed_index_endpoint_GET_request_returns_list(self):
        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )

        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.get(url)
        data = json.loads(response.content.decode())

        self.assertIsInstance(data, list)

    @mock.patch.object(FeedManager, 'fetch_source')
    def test_feed_index_endpoint_POST_request_creates_new_feed_object(self, fetch_source):
        with open(os.path.join(settings.PROJECT_DIR, 'core', 'tests', 'data', 'feed.xml')) as xmlfile:
            fetch_source.return_value = feedparser.parse(xmlfile.read())

        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )
        data = {'href': 'http://example.com/feed/'}
        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

    def test_details_endpoint_PATCH_request_updates_and_returns_object(self):
        feed = FeedFactory(user=self.simple_user)
        url = reverse('feedthing-api-v1-feed-details', kwargs={'feed_id': feed.uid})
        data = {'title': 'This is new title'}
        self.assertNotEqual(feed.title, data['title'])

        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        feed.refresh_from_db()
        self.assertEqual(feed.title, data['title'])
        self.assertEqual(response.data['title'], data['title'])

    @mock.patch.object(FeedManager, 'fetch_source')
    def test_details_endpoint_POST_request_updates_and_returns_object(self, fetch_source):
        with open(os.path.join(settings.PROJECT_DIR, 'core', 'tests', 'data', 'feed.xml')) as xmlfile:
            fetch_source.return_value = feedparser.parse(xmlfile.read())

        feed = FeedFactory(user=self.simple_user)
        last_fetch_before = feed.last_fetch
        url = reverse('feedthing-api-v1-feed-details', kwargs={'feed_id': feed.uid})
        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        feed.refresh_from_db()
        self.assertTrue(last_fetch_before < feed.last_fetch)

    def test_details_endpoint_DELETE_request_deletes_object(self):
        feed = FeedFactory(user=self.simple_user)
        feed_id = feed.uid
        url = reverse('feedthing-api-v1-feed-details', kwargs={'feed_id': feed.uid})

        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Feed.objects.filter(uid=feed_id).exists())
