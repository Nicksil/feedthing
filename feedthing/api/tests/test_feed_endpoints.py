from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories import UserFactory


class FeedEndpointsTests(APITestCase):
    def setUp(self):
        self.simple_user_pw = 'simple_password'
        self.simple_user = UserFactory(password=self.simple_user_pw)

    def test_feed_index_GET_request_returns_status_200(self):
        self.client.login(
            username=self.simple_user.email,
            password=self.simple_user_pw,
        )

        url = reverse('feedthing-api-v1-feed-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
