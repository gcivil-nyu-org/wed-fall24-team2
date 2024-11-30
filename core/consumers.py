import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")

        # If user is not authenticated, close the connection
        if not user or not user.is_authenticated:
            logger.warning(
                "Unauthenticated user attempted to connect to Notification WebSocket."
            )
            await self.close(code=4001)
            return

        # Add the user to their personal notification group
        self.user_group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.accept()
        logger.info(f"Notification WebSocket connected for user {user.id}")

    async def disconnect(self, close_code):
        # Remove the user from their notification group
        if hasattr(self, "user_group_name"):
            await self.channel_layer.group_discard(
                self.user_group_name, self.channel_name
            )

        logger.info(
            f"Notification WebSocket disconnected for user, Close Code: {close_code}"
        )

    async def logout_message(self, event):
        """
        Handle logout notifications sent to this user.
        """
        logger.info(f"Logout message received for user {self.scope['user'].id}")
        # Close the WebSocket with a custom code for logout
        await self.close(code=4001)
