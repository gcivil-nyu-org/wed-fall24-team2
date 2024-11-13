from django.test import TestCase
from django.contrib.auth.models import User
from chatroom.models import Chatroom, ChatMessage


class ChatroomModelTests(TestCase):
    def setUp(self):
        self.chatroom = Chatroom.objects.create(
            name="Test Chatroom",
            address="123 Test Street",
            city="Test City",
            state="Test State",
            country="Test Country",
            zipcode="12345",
            description="This is a test chatroom description.",
            latitude=12.345678,
            longitude=98.765432,
        )

    def test_chatroom_str(self):
        # Check if the string representation of the chatroom is correct
        self.assertEqual(str(self.chatroom), "Test Chatroom")

    def test_chatroom_fields(self):
        # Check if the fields are correctly set
        self.assertEqual(self.chatroom.address, "123 Test Street")
        self.assertEqual(self.chatroom.city, "Test City")
        self.assertEqual(self.chatroom.state, "Test State")
        self.assertEqual(self.chatroom.country, "Test Country")
        self.assertEqual(self.chatroom.zipcode, "12345")
        self.assertEqual(
            self.chatroom.description, "This is a test chatroom description."
        )
        self.assertEqual(self.chatroom.latitude, 12.345678)
        self.assertEqual(self.chatroom.longitude, 98.765432)


class ChatMessageModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.chatroom = Chatroom.objects.create(
            name="Test Chatroom",
            latitude=12.345678,
            longitude=98.765432,
        )
        self.chat_message = ChatMessage.objects.create(
            chatroom=self.chatroom,
            user=self.user,
            message="This is a test message",
        )

    def test_chat_message_str(self):
        # Check if the string representation of the chat message is correct
        expected_str = "testuser: This is a test messa... in Test Chatroom"
        self.assertEqual(str(self.chat_message), expected_str)

    def test_chat_message_fields(self):
        # Check if the fields are correctly set
        self.assertEqual(self.chat_message.chatroom, self.chatroom)
        self.assertEqual(self.chat_message.user, self.user)
        self.assertEqual(self.chat_message.message, "This is a test message")
        self.assertIsNotNone(
            self.chat_message.timestamp
        )  # Check if timestamp is auto-generated
