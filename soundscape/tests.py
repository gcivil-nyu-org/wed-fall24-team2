from django.test import TestCase, Client
from django.urls import reverse
from chatroom.models import Chatroom
import json
import os


class HomepageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        os.environ["MAPBOX_ACCESS_TOKEN"] = "test_token"
        self.chatroom = Chatroom.objects.create(
            name="Test Chatroom", latitude=40.72, longitude=-74.02
        )

    def test_homepage_view(self):
        response = self.client.get(reverse("soundscape:homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("mapbox_access_token", response.context)
        self.assertEqual(response.context["mapbox_access_token"], "test_token")
        expected_chatroom_data = [
            {
                "address": None,
                "city": None,
                "country": None,
                "description": None,
                "id": 1,
                "latitude": 40.72,
                "longitude": -74.02,
                "name": "Test Chatroom",
                "state": None,
                "zipcode": None,
            }
        ]
        self.assertJSONEqual(
            response.context["chatrooms"], json.dumps(expected_chatroom_data)
        )

        self.assertEqual(response.context["username"], "")

        sound_data = json.loads(response.context["sound_data"])
        self.assertIsInstance(sound_data, list)
        self.assertEqual(len(sound_data), 2000)

    def tearDown(self):
        Chatroom.objects.all().delete()
