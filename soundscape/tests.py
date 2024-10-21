from django.test import TestCase, Client
from django.urls import reverse
from chatroom.models import Chatroom
from sounddata_s3.models import NYCSoundFile
import json
import os


class HomepageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        os.environ["MAPBOX_ACCESS_TOKEN"] = "test_token"
        self.sound_file = NYCSoundFile.objects.create(
            unique_key="test_key",
            latitude=40.7128,
            longitude=-74.0060,
            sound_file_url="http://example.com/sound.mp3",
        )
        self.chatroom = Chatroom.objects.create(
            name="Test Chatroom", latitude=40.72, longitude=-74.02
        )

    def test_homepage_view(self):
        response = self.client.get(reverse("soundscape:homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("mapbox_access_token", response.context)
        self.assertEqual(response.context["mapbox_access_token"], "test_token")
        expected_sound_data = [
            {
                "unique_key": self.sound_file.unique_key,
                "latitude": self.sound_file.latitude,
                "longitude": self.sound_file.longitude,
                "sound_file_url": self.sound_file.sound_file_url,
            }
        ]
        self.assertJSONEqual(
            response.context["sound_data"], json.dumps(expected_sound_data)
        )
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

        self.assertEqual(
            response.context["username"], ""
        )

    def tearDown(self):
        NYCSoundFile.objects.all().delete()
        Chatroom.objects.all().delete()
