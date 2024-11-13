from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_index_view(self):
        # Use the reverse function to get the URL of the index view
        response = self.client.get(reverse("index"))

        # Check that the response returns a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response content is as expected
        self.assertContains(response, "Hello, world. You're at the polls index.")
