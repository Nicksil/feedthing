import json

from django.test import TestCase
from django.urls import reverse

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
