import uuid

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from feeds.tests.factories import FeedFactory
from users.tests.factories import UserFactory


class APIBaseTestCase(TestCase):
    def setUp(self):
        self.test_user_pw = 'test_pw'
        self.test_user = UserFactory(password=self.test_user_pw)
        self.test_feed = FeedFactory()

    def test_Endpoint_get_object_returns_object(self):
        url = reverse('feedthing-api-v1-feed-details', kwargs={'feed_id': self.test_feed.id})
        client = APIClient()
        client.login(email=self.test_user.email, password=self.test_user_pw)

        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(self.test_feed.id))

    def test_Endpoint_returns_correct_response_when_resource_does_not_exist(self):
        url = reverse('feedthing-api-v1-feed-details', kwargs={'feed_id': str(uuid.uuid4())})
        client = APIClient()
        client.login(email=self.test_user.email, password=self.test_user_pw)

        response = client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Resource does not exist.')
