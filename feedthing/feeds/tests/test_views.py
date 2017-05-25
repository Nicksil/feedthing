from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory


class FeedsViewsTestCase(TestCase):
    def setUp(self):
        self.simple_user_pw = 'simple_password'
        self.simple_user = UserFactory(password=self.simple_user_pw)
        self.rss_url = 'http://djangopackages.com/feeds/packages/latest/rss/'

    def test_index_view_handles_a_get_request(self):
        self.client.login(email=self.simple_user.email, password=self.simple_user_pw)

        url = reverse('feeds:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_feed_view_handles_a_post_request(self):
        self.client.login(email=self.simple_user.email, password=self.simple_user_pw)
        url = reverse('feeds:add_feed')
        response = self.client.post(url, data={'href': self.rss_url})
        expected_url = reverse('feeds:index')
        self.assertRedirects(response, expected_url, target_status_code=200)
