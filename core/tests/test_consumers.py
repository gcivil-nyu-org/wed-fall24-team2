import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from django.contrib.auth.models import User, AnonymousUser
from django.test import TransactionTestCase
from core.asgi import application
import logging

# Silence the logging during the tests
logging.disable(logging.CRITICAL)


class NotificationConsumerTest(TransactionTestCase):
    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    @pytest.mark.asyncio
    async def test_unauthenticated_user_connect(self):
        """Test that an unauthenticated user cannot connect to the WebSocket."""
        communicator = WebsocketCommunicator(application, "/ws/notifications/")
        communicator.scope["user"] = AnonymousUser()  # Simulate an unauthenticated user

        # Manually add channel layer to the communicator
        communicator.scope["channel_layer"] = get_channel_layer()

        # Attempt to connect to the WebSocket
        connected, _ = await communicator.connect()

        # Since the user is not authenticated, they should not be able to connect
        assert not connected, "Unauthenticated user should not be allowed to connect"

        # Disconnect cleanly if somehow connected (just in case)
        if connected:
            await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_authenticated_user_connect(self):
        """Test that an authenticated user can connect to the WebSocket."""
        communicator = WebsocketCommunicator(application, "/ws/notifications/")
        communicator.scope["user"] = self.user  # Simulate an authenticated user

        # Manually add channel layer to the communicator
        communicator.scope["channel_layer"] = get_channel_layer()

        connected, _ = await communicator.connect()

        # Since the user is authenticated, they should be able to connect
        assert connected, "Authenticated user should be able to connect"

        # Disconnect cleanly
        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_authenticated_user_disconnect(self):
        """Test that an authenticated user can disconnect from the WebSocket."""
        communicator = WebsocketCommunicator(application, "/ws/notifications/")
        communicator.scope["user"] = self.user  # Simulate an authenticated user

        # Manually add channel layer to the communicator
        communicator.scope["channel_layer"] = get_channel_layer()

        connected, _ = await communicator.connect()
        assert connected, "Authenticated user should be able to connect"

        # Disconnect the WebSocket
        await communicator.disconnect()
