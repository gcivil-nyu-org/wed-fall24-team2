import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from core.asgi import application
from chatroom.models import Chatroom


class ChatRoomConsumerTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.chatroom = Chatroom.objects.create(
            name="Test Room", latitude=40.7128, longitude=-74.0060
        )

    @pytest.mark.asyncio
    async def test_connect_and_receive_message(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/chatroom/{self.chatroom.name}/"
        )
        communicator.scope["user"] = self.user

        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected

        # Send a message to the consumer
        message = {"message": "Hello, world!", "timestamp": "2024-11-12T12:34:56Z"}
        await communicator.send_json_to(message)

        # Receive the message sent back
        try:
            response = await communicator.receive_json_from()
            print("Received response:", response)  # Debugging output
            assert response["message"] == "Hello, world!"
            assert response["username"] == "testuser"
            assert response["timestamp"] == "2024-11-12T12:34:56Z"
        except KeyError as e:
            print(f"KeyError: {e}")

        # Disconnect the WebSocket
        await communicator.disconnect()

    def tearDown(self):
        self.user.delete()
        self.chatroom.delete()

    @pytest.mark.asyncio
    async def test_disconnect(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/chatroom/{self.chatroom.name}/"
        )
        communicator.scope["user"] = self.user

        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        assert connected

        # Disconnect the WebSocket
        await communicator.disconnect()
        # Optionally, you can check if any log messages or clean-up actions were performed

    @pytest.mark.asyncio
    async def test_json_decode_error(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/chatroom/{self.chatroom.name}/"
        )
        communicator.scope["user"] = self.user

        # Connect to the WebSocket
        connected, _ = await communicator.connect(timeout=10)
        assert connected

        # Send an invalid JSON message
        await communicator.send_to(text_data="Invalid JSON String")

        # Check the logs or behavior to ensure the error is handled
        # You can add logging checks if necessary

        # Disconnect the WebSocket
        await communicator.disconnect()
