import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.utils.timesince import timesince

from .templatetags.chatextras import initials

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

    
    async def receive(self, text_data):
        # Recieve message from the websocket
        text_data_json  = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent', '')

        print('Recieve: ', type)
        # send message to group/ room

        # if text_data_json["type"] == 'fetch_message':
        #     print('fetch.....?')
        #     pass
        # elif text_data_json["type"] == 'chat_message':
         # await self.channel_layer.group_send(self.room_group_name, text_data_json)
        if type == 'message':
           
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'name': name,
                'agent': agent,
                'initials': initials(name),
                'created_at': ' ' #timesince(new_message.created_at),
            })

    #must be same at the type value in json data 
    async def chat_message(self, event):
        # Send message to WebSocket (front end)

        # await self.send(text_data=json.dumps(event))

        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'agent': event['agent'],
            'initials': event['initials'],
            'created_at': event['created_at'],
        }))
