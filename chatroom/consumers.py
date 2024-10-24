import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
        self.room_group_name = f"chat_{self.chatroom_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(
            f"Connected to room: {self.chatroom_name}, Group Name: {self.room_group_name}"
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"Disconnected from room: {self.chatroom_name}, Code: {close_code}")

    async def receive(self, text_data):
        logger.info(f"Text data received: {text_data}")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "")
            username = text_data_json.get("username", "Anonymous")
            timestamp = text_data_json.get("timestamp", "N/A")

            # Send message to room group
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
