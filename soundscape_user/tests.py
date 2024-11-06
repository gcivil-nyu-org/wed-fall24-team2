# from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from .models import SoundFileUser
import json


class SoundFileUploadTest(TestCase):
    @patch("boto3.client")
    def test_upload_sound_file_valid(self, mock_boto_client):
        mock_s3 = mock_boto_client.return_value
        mock_s3.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        sound_file = SimpleUploadedFile(
            "test_sound.mp3", b"file_content", content_type="audio/mp3"
        )
        data = {
            "username": "test_user",
            "sound_file": sound_file,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "sound_descriptor": "ambient_noise",
        }

        response = self.client.post(reverse("upload_sound_file"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Sound uploaded successfully")
        self.assertTrue(SoundFileUser.objects.filter(user_name="test_user").exists())

    @patch("boto3.client")
    def test_upload_sound_file_invalid_size(self, mock_boto_client):
        # mock_s3 = mock_boto_client.return_value

        # Creating a file that exceeds 3 MB
        sound_file = SimpleUploadedFile(
            "test_sound.mp3", b"file_content" * 1000000, content_type="audio/mp3"
        )
        data = {
            "username": "test_user",
            "sound_file": sound_file,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "sound_descriptor": "ambient_noise",
        }

        response = self.client.post(reverse("upload_sound_file"), data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"], "Please limit the sound file size to 3 MB"
        )

    @patch("boto3.client")
    def test_upload_sound_file_invalid_method(self, mock_boto_client):
        # mock_s3 = mock_boto_client.return_value
        sound_file = SimpleUploadedFile(
            "test_sound.mp3", b"file_content", content_type="audio/mp3"
        )
        data = {
            "username": "test_user",
            "sound_file": sound_file,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "sound_descriptor": "ambient_noise",
        }

        response = self.client.get(reverse("upload_sound_file"), data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["error"], "Invalid request method")


class SoundFileLocationTest(TestCase):
    def setUp(self):
        self.sound_file = SoundFileUser.objects.create(
            user_name="test_user",
            sound_descriptor="ambient_noise",
            s3_file_name="user_sounds/test_user_20231106.mp3",
            latitude=40.7128,
            longitude=-74.0060,
        )

    def test_sounds_at_location_valid(self):
        response = self.client.get(
            reverse("sounds_at_location", kwargs={"lat": 40.7128, "lng": -74.0060})
        )
        self.assertEqual(response.status_code, 200)

        sounds = response.json().get("sounds")
        self.assertEqual(len(sounds), 1)
        self.assertEqual(sounds[0]["user_name"], "test_user")
        self.assertEqual(sounds[0]["sound_descriptor"], "ambient_noise")
        self.assertTrue(sounds[0]["listen_link"].endswith(self.sound_file.s3_file_name))

    def test_sounds_at_location_invalid_method(self):
        response = self.client.post(
            reverse("sounds_at_location", kwargs={"lat": 40.7128, "lng": -74.0060})
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["error"], "Invalid request method")


class SoundFileDeleteTest(TestCase):
    @patch("boto3.client")
    def test_delete_sound_file(self, mock_boto_client):
        mock_s3 = mock_boto_client.return_value
        mock_s3.delete_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 204}
        }

        # sound_file = SoundFileUser.objects.create(
        #     user_name="test_user",
        #     sound_descriptor="ambient_noise",
        #     s3_file_name="user_sounds/test_user_20231106.mp3",
        #     latitude=40.7128,
        #     longitude=-74.0060,
        # )

        data = json.dumps(
            {
                "user_name": "test_user",
                "sound_name": "user_sounds/test_user_20231106.mp3",
            }
        )
        response = self.client.post(
            reverse("delete_sound_file"), data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertFalse(
            SoundFileUser.objects.filter(
                s3_file_name="user_sounds/test_user_20231106.mp3"
            ).exists()
        )

    # @patch("boto3.client")
    # def test_delete_sound_file_not_found(self, mock_boto_client):
    #     mock_s3 = mock_boto_client.return_value
    #     mock_s3.delete_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 204}}

    #     sound_file = SoundFileUser.objects.create(
    #         user_name="test_user",
    #         sound_descriptor="ambient_noise",
    #         s3_file_name="user_sounds/test_user_20231106.mp3",
    #         latitude=40.7128,
    #         longitude=-74.0060,
    #     )

    #     data = json.dumps({"user_name": "test_user", "sound_name": "non_existent_sound.mp3"})
    #     response = self.client.post(reverse("delete_sound_file"), data, content_type="application/json")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["status"], "success")
    #     self.assertTrue(SoundFileUser.objects.filter(s3_file_name="user_sounds/test_user_20231106.mp3").exists())

    # def test_delete_sound_file_invalid_method(self):
    #     data = json.dumps({"user_name": "test_user", "sound_name": "user_sounds/test_user_20231106.mp3"})
    #     response = self.client.get(reverse("delete_sound_file"), data, content_type="application/json")
    #     self.assertEqual(response.status_code, 405)
    #     self.assertEqual(response.json()["error"], "Invalid request method")
