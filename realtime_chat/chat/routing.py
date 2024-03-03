from django.urls import path

from .consumers import ChatConsumer

#what does not make asgi run on server sometimes after configurations is the channels/ daphane/ django version

websocket_urlpatterns = [
    path("ws/<str:room_name>/", ChatConsumer.as_asgi()),
]