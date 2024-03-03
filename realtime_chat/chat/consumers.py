import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

#what does not make asgi run on server sometimes after configurations is the channels/ daphane/ django version

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #for the web socket url params
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        #add a room to the channel
        self.room_group_name = f'chat_{self.room_name}'
        #join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #accept
        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)