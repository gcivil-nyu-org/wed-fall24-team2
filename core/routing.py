from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, include

from core.consumers import NotificationConsumer
from chatroom.routing import websocket_urlpatterns as chatroom_websocket_patterns

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/notifications/", NotificationConsumer.as_asgi()),
                    *chatroom_websocket_patterns,  # Include chatroom WebSocket routes
                ]
            )
        ),
    }
)
