import json
import logging
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Chatroom, ChatMessage
import urllib.parse

logger = logging.getLogger(__name__)


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_name = urllib.parse.unquote(
            self.scope["url_route"]["kwargs"]["chatroom_name"]
        )
        self.room_group_name = f"chat_{self.chatroom_name.replace(' ', '_')}"

        # Validate user session
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            logger.warning("Unauthenticated user attempted to connect.")
            await self.close(code=4001)  # Custom WebSocket close code
            return

        # Add the user to their personal group for logout handling
        self.user_group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        # Add user to the chatroom group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"Connected to room: {self.chatroom_name}")
        await self.send_chat_history()

    async def disconnect(self, close_code):
        try:
            if self.scope.get("user") and self.scope["user"].is_authenticated:
                logger.info(f"User {self.scope['user'].username} disconnected.")

            # Remove from groups
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
            if hasattr(self, "user_group_name"):
                await self.channel_layer.group_discard(
                    self.user_group_name, self.channel_name
                )

            # Handle close code specifics
            if close_code == 4001:
                logger.warning("Disconnected due to session expiry.")
            elif close_code == 1000:
                logger.info("Normal WebSocket closure.")
            else:
                logger.debug(f"Disconnected with code: {close_code}")

            logger.info(
                f"Disconnected from room: {self.chatroom_name}, Code: {close_code}"
            )
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")

    async def logout_message(self, event):
        # Handle logout notification
        logger.info("Received logout message. Closing WebSocket connection.")
        await self.close(code=4001)

    async def receive(self, text_data):
        logger.info(f"Text data received: {text_data}")
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            logger.error("Unauthenticated user cannot send messages.")
            await self.send(
                text_data=json.dumps(
                    {"error": "Unauthenticated. Redirecting to login."}
                )
            )
            await self.close(code=4001)  # Close connection for unauthenticated user
            return

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "")
            username = user.username
            timestamp = text_data_json.get("timestamp", "N/A")

            chatroom = await Chatroom.objects.aget(name=self.chatroom_name)
            await ChatMessage.objects.acreate(
                chatroom=chatroom, user=user, message=message
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "timestamp": timestamp,
                },
            )
            logger.info(f"Group Send Triggered: {message} from {username}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
        except User.DoesNotExist:
            logger.error("User does not exist.")
            await self.send(text_data=json.dumps({"error": "User does not exist"}))
        except Chatroom.DoesNotExist:
            logger.error("Chatroom does not exist.")
            await self.send(text_data=json.dumps({"error": "Chatroom does not exist"}))

    async def chat_message(self, event):
        logger.info(f"Chat message event received: {event}")
        message = event.get("message", "")
        username = event.get("username", "Unknown")
        timestamp = event.get("timestamp", "Unknown")

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "username": username, "timestamp": timestamp}
            )
        )
        logger.info(f"Sent message: {message} from {username} at {timestamp}")

    async def send_chat_history(self, page=1, messages_per_page=50):
        try:
            chatroom = await Chatroom.objects.aget(name=self.chatroom_name)

            offset = (page - 1) * messages_per_page
            recent_messages = await sync_to_async(
                lambda: list(
                    ChatMessage.objects.filter(chatroom=chatroom)
                    .order_by("-timestamp")[offset : offset + messages_per_page]
                    .values("message", "user__username", "timestamp")
                )
            )()

            # Process messages for the chat history
            history = [
                {
                    "message": msg["message"],
                    "username": msg["user__username"],
                    "timestamp": msg["timestamp"].isoformat(),
                }
                for msg in recent_messages
            ]

            # Send chat history to WebSocket
            await self.send(text_data=json.dumps({"history": history, "page": page}))
        except Chatroom.DoesNotExist:
            logger.error(f"Chatroom {self.chatroom_name} does not exist.")
            await self.send(text_data=json.dumps({"error": "Chatroom does not exist"}))
            await self.close()
