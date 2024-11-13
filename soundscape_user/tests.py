from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class SoundscapeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_datetime = datetime(2024, 1, 1, 12, 0, 0)

    @patch('soundscape_user.views.s3')
    @patch('soundscape_user.views.datetime')
    def test_upload_sound_file_success(self, mock_datetime, mock_s3):
        # Mock datetime
        mock_datetime.now.return_value = self.mock_datetime

        # Create test file
        test_file = SimpleUploadedFile(
            "test.mp3",
            b"file_content",
            content_type="audio/mpeg"
        )

        # Prepare form data
        form_data = {
            'username': 'testuser',
            'latitude': '40.7128',
            'longitude': '-74.0060',
            'sound_descriptor': 'test sound'
        }
        file_data = {'sound_file': test_file}

        response = self.client.post(
            reverse('upload_sound_file'),
            {**form_data, **file_data}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"message": "Sound uploaded successfully"}
        )

        # Verify S3 upload was called
        mock_s3.put_object.assert_called_once()

    def test_upload_sound_file_large_file(self):
        # Create large test file (4MB)
        large_file = SimpleUploadedFile(
            "large.mp3",
            b"0" * (4 * 1024 * 1024),
            content_type="audio/mpeg"
        )

        form_data = {
            'username': 'testuser',
            'latitude': '40.7128',
            'longitude': '-74.0060',
            'sound_descriptor': 'test sound'
        }
        file_data = {'sound_file': large_file}

        response = self.client.post(
            reverse('upload_sound_file'),
            {**form_data, **file_data}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"error": "Please limit the sound file size to 3 MB"}
        )

    @patch('soundscape_user.views.SoundFileUser.objects')
    def test_sounds_at_location(self, mock_sounds):
        # Mock database query
        mock_sound = MagicMock()
        mock_sound.user_name = 'testuser'
        mock_sound.sound_descriptor = 'test sound'
        mock_sound.s3_file_name = 'test.mp3'
        mock_sound.created_at = self.mock_datetime
        mock_sounds.filter.return_value = [mock_sound]

        response = self.client.get(
            reverse('sounds_at_location', kwargs={'lat': '40.7128', 'lng': '-74.0060'})
        )

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['sounds']), 1)

    @patch('soundscape_user.views.s3')
    def test_delete_sound_file_success(self, mock_s3):
        # Mock S3 check and delete
        mock_s3.get_object.return_value = True

        sound_data = {
            'user_name': 'testuser',
            'sound_name': 'test.mp3'
        }

        response = self.client.post(
            reverse('delete_sound_file'),
            json.dumps(sound_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"status": "success"}
        )

    @patch('soundscape_user.views.SoundFileUser.objects')
    def test_sounds_for_user(self, mock_sounds):
        # Mock database query
        mock_sound = MagicMock()
        mock_sound.user_name = 'testuser'
        mock_sound.sound_descriptor = 'test sound'
        mock_sound.s3_file_name = 'test.mp3'
        mock_sound.created_at = self.mock_datetime
        mock_sounds.filter.return_value.order_by.return_value = [mock_sound]

        response = self.client.get(
            reverse('sounds_for_user', kwargs={'user_name': 'testuser'})
        )

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['sounds']), 1)