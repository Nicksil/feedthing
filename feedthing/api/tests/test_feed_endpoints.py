from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory


class FeedEndpointsTests(TestCase):
    def setUp(self):
        self.simple_user_pw = 'simple_password'
        self.simple_user = UserFactory(password=self.simple_user_pw)

    def test_feed_index_GET_request_returns_status_200(self):
        # self.client.login(
        #     email=self.simple_user.email,
        #     password=self.simple_user_pw,
        # )

        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
