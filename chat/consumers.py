import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.utils.timesince import timesince

from .templatetags.chatextras import initials

from account.models import User

from .models import Room, Message

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
        #     new_message = await self.create_message(name, message, agent)
        #     await self.channel_layer.group_send(self.room_group_name, text_data_json)
        if type == 'message':
            new_message = await self.create_message(name, message, agent)
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'name': name,
                'agent': agent,
                'initials': initials(name),
                'created_at':  timesince(new_message.created_at),
            })

    #must be same at the type value in json data 
    async def chat_message(self, event):
        # Send message to WebSocket (front end)

        #better still you can write the algrothim here to save to db other than writing some functions below
        # this algo does not go inline with the code db or codebade(just a guide to how it can be done)

        # room = Room.objects.get(room_name = self.scope["url_route"]["kwargs"]["room_name"])
        # sender = User.objects.get(username=self.scope["url_route"]["kwargs"]["sender"]).user #get user through the param of th websocket (username)
        # Message.objects.create(
        #     body= event['message'],
        #     sent_by= 'heyy',
        #     created_by= sender,
        #     room = room,
        # )

        # await self.send(text_data=json.dumps(event))

        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'agent': event['agent'],
            'initials': event['initials'],
            'created_at': event['created_at'],
        }))


    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid=self.room_name)



    @sync_to_async
    def create_message(self, sent_by, message, agent):
        message = Message.objects.create(body=message, sent_by=sent_by)

        if agent:
            message.created_by = User.objects.get(pk=agent)
            message.save()
        
        # self.room.messages.add(message)

        return message
