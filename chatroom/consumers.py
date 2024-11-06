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

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(
            f"Connected to room: {self.chatroom_name}, Group Name: {self.room_group_name}"
        )
        print(
            f"Connected to room: {self.chatroom_name}, Group Name: {self.room_group_name}"
        )
        await self.send_chat_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"Disconnected from room: {self.chatroom_name}, Code: {close_code}")

    async def receive(self, text_data):
        logger.info(f"Text data received: {text_data}")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "")
            user = self.scope.get("user")

            # Check if user is authenticated and exists
            if user is None or not user.is_authenticated:
                logger.error("Unauthenticated user cannot send messages.")
                await self.send(
                    text_data=json.dumps({"error": "User not authenticated"})
                )
                return

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
        message = event["message"]  # Added to fix the undefined 'message'
        username = event["username"]
        timestamp = event["timestamp"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "username": username, "timestamp": timestamp}
            )
        )
        logger.info(f"Sent message: {message} from {username} at {timestamp}")

    async def send_chat_history(self, page=1, messages_per_page=50):
        chatroom = await Chatroom.objects.aget(name=self.chatroom_name)

        offset = (page - 1) * messages_per_page
        # Use sync_to_async to make the ORM query async-compatible
        recent_messages = await sync_to_async(
            lambda: list(
                ChatMessage.objects.filter(chatroom=chatroom)
                .order_by("-timestamp")[offset : offset + messages_per_page]
                .values("message", "user__username", "timestamp")
            )
        )()

        # Process the messages to create the history list
        history = [
            {
                "message": msg["message"],
                "username": msg["user__username"],
                "timestamp": msg["timestamp"].isoformat(),
            }
            for msg in recent_messages
        ]

        # Send the chat history to the WebSocket
        await self.send(text_data=json.dumps({"history": history, "page": page}))
