import os
from django.core.asgi import get_asgi_application

#Seems to fail due to the model imports in my consumers.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatroom.routing


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(chatroom.routing.websocket_urlpatterns)
        ),
    }
)
