from django.test import TestCase
from django.urls import reverse


class ChatroomViewTests(TestCase):
    def test_chatroom_view_status_code(self):
        # Simulate a request to the chatroom view with a chatroom name
        response = self.client.get(reverse("chatroom", args=["test-room"]))
        self.assertEqual(response.status_code, 200)

    def test_chatroom_view_template_used(self):
        # Simulate a request to the chatroom view
        response = self.client.get(reverse("chatroom", args=["test-room"]))
        self.assertTemplateUsed(response, "chatroom.html")

    def test_chatroom_view_context(self):
        # Simulate a request to the chatroom view with a chatroom name
        chatroom_name = "test-room"
        response = self.client.get(reverse("chatroom", args=[chatroom_name]))
        self.assertEqual(response.context["chatroom_name"], chatroom_name)
