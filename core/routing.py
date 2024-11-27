from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from core.consumers import NotificationConsumer
from chatroom.routing import websocket_urlpatterns as chatroom_websocket_patterns
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    *chatroom_websocket_patterns,  # Include chatroom WebSocket routes
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
