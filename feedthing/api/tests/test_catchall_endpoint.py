from django.test import TestCase
from django.urls import reverse


class APICatchallEndpointTestCase(TestCase):
    def test_catchall_endpoint_returns_status_404_and_correct_message(self):
        url = reverse('feedthing-api-v1-catchall')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Nothing exists here.')
