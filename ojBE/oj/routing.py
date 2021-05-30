from .wsgi import *
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from battle.consumers import BattleConsumer

application = ProtocolTypeRouter({
    "http" : get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/battle/', BattleConsumer.as_asgi()),
        ])
    ),
})