import json

from django.core import serializers
from django.test import TestCase
from django.urls import reverse

from feeds.tests.factories import EntryFactory
from feeds.tests.factories import FeedFactory
from users.tests.factories import UserFactory


class APIEntryEndpointsTestCase(TestCase):
    def setUp(self):
        self.simple_user_pw = 'simple_password'
        self.simple_user = UserFactory(password=self.simple_user_pw)
        self.test_feed = FeedFactory(user=self.simple_user)
        self.test_entry = EntryFactory(feed=self.test_feed)

    def test_detail_endpoint_GET_request_returns_correct_data(self):
        url = reverse(
            'feedthing-api-v1-entry-details',
            kwargs={
                'feed_uid': self.test_feed.uid,
                'entry_uid': self.test_entry.uid
            }
        )
        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['uid'], self.test_entry.uid)

    def test_detail_endpoint_PATCH_request_modifies_and_returns_object(self):
        url = reverse(
            'feedthing-api-v1-entry-details',
            kwargs={
                'feed_uid': self.test_feed.uid,
                'entry_uid': self.test_entry.uid
            }
        )
        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )

        data = {'title': 'This is new title'}
        self.assertNotEqual(self.test_entry.title, data['title'])

        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], data['title'])

        self.test_entry.refresh_from_db()
        self.assertEqual(self.test_entry.title, data['title'])

    def test_detail_endpoint_PUT_request_modifies_and_returns_object(self):
        url = reverse(
            'feedthing-api-v1-entry-details',
            kwargs={
                'feed_uid': self.test_feed.uid,
                'entry_uid': self.test_entry.uid
            }
        )
        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )

        # FIXME: There has got to be a batter way of doing this
        data = json.loads(serializers.serialize('json', [self.test_entry]))[0]
        data['href'] = 'http://a-new-href.com'
        self.assertNotEqual(self.test_entry.href, data['href'])

        response = self.client.put(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['href'], data['href'])

        self.test_entry.refresh_from_db()
        self.assertEqual(self.test_entry.href, data['href'])

    def test_index_endpoint_GET_request_returns_entry_objects(self):
        url = reverse(
            'feedthing-api-v1-entry-index',
            kwargs={'feed_uid': self.test_feed.uid}
        )
        self.client.login(
            email=self.simple_user.email,
            password=self.simple_user_pw,
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIn(self.test_entry.uid, [e['uid'] for e in response.data])
