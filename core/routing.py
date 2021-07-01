from django.urls import path, include

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from game import routing


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(routing.ws_urlpatterns)
    ),
})