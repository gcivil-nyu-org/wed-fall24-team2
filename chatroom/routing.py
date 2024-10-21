from django.urls import re_path
from . import consumers

# WebSocket URLs that handle the connection for chatrooms
websocket_urlpatterns = [
    re_path(
        r"ws/chatroom/(?P<chatroom_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()
    ),
]
