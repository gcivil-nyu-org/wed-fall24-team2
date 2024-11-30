import os
from django.core.asgi import get_asgi_application

# Set the default settings module before calling get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_asgi_application()


# Lazy import of Channels and routing after Django application setup
def get_application():
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    import core.routing

    return ProtocolTypeRouter(
        {
            "http": get_asgi_application(),
            "websocket": AuthMiddlewareStack(
                URLRouter(core.routing.websocket_urlpatterns)
            ),
        }
    )


application = get_application()
