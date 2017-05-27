from unittest import mock
import json
import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

import feedparser

from feeds.managers import FeedManager
from feeds.models import Feed
from feeds.tests.factories import FeedFactory
from users.tests.factories import UserFactory


class FeedEndpointsTests(TestCase):
    def _get_feed(self):
        with open(os.path.join(settings.PROJECT_DIR, 'core', 'tests', 'data', 'feeds', 'rss_2_0.xml')) as xmlfile:
            return feedparser.parse(xmlfile.read())

    def _login(self):
        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )

    def setUp(self):
        self.simple_user_pw = 'simple_password'
        self.simple_user = UserFactory(password=self.simple_user_pw)

    def test_feed_index_endpoint_GET_request_returns_list(self):
        self._login()

        # Request
        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.get(url)

        self.assertIsInstance(json.loads(response.content.decode()), list)

    @mock.patch.object(FeedManager, 'fetch_source')
    def test_feed_index_endpoint_POST_request_creates_new_Feed(self, fetch_source):
        self._login()

        # Mock response from FeedManager
        fetch_source.return_value = self._get_feed()

        # Count of Feed objects before operation
        before_count = Feed.objects.count()

        # Request
        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.post(url, data=json.dumps({'href': 'http://example.com'}), content_type='application/json')

        # Ensure we're getting correct HTTP status code for an object having just been created
        self.assertEqual(response.status_code, 201)

        # Ensure we now have an additional Feed object
        self.assertTrue(Feed.objects.count() == before_count + 1)

    def test_feed_index_endpoint_POST_request_returns_error_and_correct_status_when_href_not_provided(self):
        self._login()

        # Count of Feed objects before operation
        before_count = Feed.objects.count()

        # Request
        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.post(url, data=json.dumps({'href': ''}), content_type='application/json')

        # Ensure we're getting correct HTTP status code for a bad request
        self.assertEqual(response.status_code, 400)

        # Ensure we're receiving an error in the response.
        self.assertIn('error', response.data)

        # Ensure no new Feed objects were created
        self.assertTrue(Feed.objects.count() == before_count)

    @mock.patch.object(FeedManager, 'fetch_source')
    def test_feed_index_endpoint_POST_request_handles_feedparser_request_status_404(self, fetch_source):
        self._login()

        # Mock response from FeedManager
        feed_data = self._get_feed()
        feed_data['status'] = 404
        fetch_source.return_value = feed_data

        # Count of Feed objects before operation
        before_count = Feed.objects.count()

        # Request
        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.post(url, data=json.dumps({'href': 'http://example.com'}), content_type='application/json')

        # Ensure we're getting correct HTTP status code for a bad request
        self.assertEqual(response.status_code, 400)

        # Ensure no new Feed objects were created
        self.assertTrue(Feed.objects.count() == before_count)

        # Ensure we're receiving an error in the response.
        self.assertIn('error', response.data)

    def test_feed_index_endpoint_POST_request_with_existing_Feed_href_returns_error(self):
        self._login()

        # Create new Feed
        href = 'http://example.com/feed/'
        feed = FeedFactory(href=href)
        feed.users.add(self.simple_user)

        # Request
        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.post(url, data=json.dumps({'href': href}), content_type='application/json')

        # Ensure we're getting correct HTTP status code for a bad request
        self.assertEqual(response.status_code, 400)

        # Ensure we're receiving an error in the response.
        self.assertIn('error', response.data)

    def test_details_endpoint_PATCH_request_updates_and_returns_object(self):
        self._login()

        # Create new Feed
        feed = FeedFactory()
        feed.users.add(self.simple_user)

        # Quick check that factor Feed did not create with same title
        data = {'title': 'This is new title'}
        self.assertNotEqual(feed.title, data['title'])

        # Request
        url = reverse('feedthing-api-v1-feed-details', kwargs={'feed_id': feed.id})
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Feed object should have been manipulated. Need to refresh from DB to get new values
        feed.refresh_from_db()

        self.assertEqual(feed.title, data['title'])
        self.assertEqual(response.data['title'], data['title'])

    def test_details_endpoint_DELETE_request_deletes_object(self):
        self._login()

        # Create new Feed
        feed = FeedFactory()
        feed.users.add(self.simple_user)

        # Grab the ID of the Feed before we delete
        feed_id = feed.id

        # Request
        url = reverse('feedthing-api-v1-feed-details', kwargs={'feed_id': feed.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Feed.objects.filter(id=feed_id).exists())
