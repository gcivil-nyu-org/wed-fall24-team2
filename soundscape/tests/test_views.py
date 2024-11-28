from django.test import TestCase, Client
from django.urls import reverse
from chatroom.models import Chatroom
from django.contrib.auth.models import User
from soundscape.forms import SignupForm
from unittest.mock import Mock, patch
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

    def tearDown(self):
        Chatroom.objects.all().delete()


class GetNoiseDataTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("soundscape:get_noise_data")
        self.sample_response_data = [
            {
                "complaint_type": "Noise",
                "created_date": "2024-01-01",
                "latitude": "40.7128",
                "longitude": "-74.0060",
            }
        ]

    @patch("soundscape.views.requests.get")
    def test_successful_request(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = self.sample_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test data
        post_data = {
            "soundType": ["Noise"],
            "dateFrom": "2024-01-01",
            "dateTo": "2024-01-31",
        }

        # Make request
        response = self.client.post(
            self.url, data=json.dumps(post_data), content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.json()["sound_data"])
        self.assertEqual(response_data, self.sample_response_data)

    @patch("soundscape.views.requests.get")
    def test_api_error_handling(self, mock_get):
        # Setup mock to raise an exception
        mock_get.side_effect = Exception("API Error")

        # Test data
        post_data = {"soundType": ["Noise"], "dateFrom": None, "dateTo": None}

        # Make request
        response = self.client.post(
            self.url, data=json.dumps(post_data), content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("Error fetching noise data", response.json()["error"])

    def test_invalid_method(self):
        # Test GET request (should fail)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["error"], "Invalid request method")

    @patch("soundscape.views.requests.get")
    def test_empty_sound_type(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = self.sample_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test data with empty soundType
        post_data = {"soundType": [], "dateFrom": None, "dateTo": None}

        # Make request
        response = self.client.post(
            self.url, data=json.dumps(post_data), content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        # Verify that default ['Noise'] was used
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]
        self.assertIn(
            "starts_with(complaint_type, 'Noise')", call_args["params"]["$where"]
        )

    @patch("soundscape.views.requests.get")
    def test_multiple_sound_types(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = self.sample_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test data with multiple sound types
        post_data = {"soundType": ["Noise", "Music"], "dateFrom": None, "dateTo": None}

        # Make request
        response = self.client.post(
            self.url, data=json.dumps(post_data), content_type="application/json"
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]
        self.assertIn(
            "starts_with(complaint_type, 'Noise')", call_args["params"]["$where"]
        )
        self.assertIn(
            "starts_with(complaint_type, 'Music')", call_args["params"]["$where"]
        )


class ProfanityViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_check_profanity_with_clean_text(self):
        response = self.client.post(
            reverse("soundscape:check_profanity"),
            data="Hello world",
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"value": "0"})

    def test_check_profanity_with_profane_text(self):
        response = self.client.post(
            reverse("soundscape:check_profanity"),
            data="This is a damn test",
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"value": "1"})

    def test_check_profanity_with_get_method(self):
        response = self.client.get(reverse("soundscape:check_profanity"))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content), {"error": "Invalid request method"}
        )

    def test_filter_profanity_with_clean_text(self):
        test_text = "Hello world"
        response = self.client.post(
            reverse("soundscape:filter_profanity"),
            data=test_text,
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"message": test_text})

    def test_filter_profanity_with_profane_text(self):
        response = self.client.post(
            reverse("soundscape:filter_profanity"),
            data="This is a damn test",
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content), {"message": "This is a **** test"}
        )

    def test_filter_profanity_with_get_method(self):
        response = self.client.get(reverse("soundscape:filter_profanity"))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content), {"error": "Invalid request method"}
        )


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("soundscape:signup")
        self.valid_user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        }

    def test_signup_page_GET(self):
        """Test that signup page loads correctly with GET request"""
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "soundscape/signup.html")
        self.assertIsInstance(response.context["form"], SignupForm)

    def test_signup_success_POST(self):
        """Test successful user registration"""
        response = self.client.post(self.signup_url, self.valid_user_data)
        self.assertRedirects(response, "/login/")
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(User.objects.count(), 1)

    def test_signup_invalid_form_POST(self):
        """Test signup with invalid form data"""
        invalid_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password1": "pass123",
            "password2": "pass456",
        }
        response = self.client.post(self.signup_url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "soundscape/signup.html")

        self.assertEqual(User.objects.count(), 0)
        self.assertTrue(response.context["form"].errors)

    def test_signup_existing_username_POST(self):
        """Test signup with already existing username"""
        User.objects.create_user(
            username="testuser", email="existing@example.com", password="TestPass123!"
        )

        response = self.client.post(self.signup_url, self.valid_user_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "soundscape/signup.html")

        self.assertEqual(User.objects.count(), 1)

        self.assertTrue(response.context["form"].errors)

    def test_csrf_token_presence(self):
        """Test that CSRF token is present in the form"""
        response = self.client.get(self.signup_url)

        self.assertContains(response, "csrfmiddlewaretoken")
