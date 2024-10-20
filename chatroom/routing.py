# chatroom/routing.py
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from . import consumers

# websocket_urlpatterns = [
#     path('ws/chat/<str:chatroom_name>/', consumers.ChatRoomConsumer.as_asgi()),
# ]

# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns=[
    re_path(
        r"ws/chatroom/(?P<chatroom_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()
    ),
]

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)