"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Ensure Django is initialized before importing any models
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Import consumers *after* django.setup()
from notification.consumer import NotificationConsumer
from chat.consumer import ChatConsumer
from Middleware.JWTAuthMiddleware import JWTAuthMiddlewareStack  # Fix middleware import

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddlewareStack(  # Fix middleware call
            URLRouter(
                [
                    path("ws/notifications/", NotificationConsumer.as_asgi()),
                    path("ws/chat/", ChatConsumer.as_asgi()),
                ]
            )
        ),
    }
)
