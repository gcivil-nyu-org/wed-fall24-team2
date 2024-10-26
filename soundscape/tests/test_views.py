from django.test import TestCase, Client
from django.urls import reverse
from chatroom.models import Chatroom
from django.contrib.auth.models import User
from soundscape.forms import SignupForm
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
