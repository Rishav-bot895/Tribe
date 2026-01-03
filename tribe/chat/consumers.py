from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from .models import ChatGroup, GroupMessage
import json


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'chat_{self.group_name}'

        user = self.scope['user']
        if user is None or isinstance(user, AnonymousUser):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("=== RECEIVE CALLED ===")
        print("RAW:", text_data)

        data = json.loads(text_data)
        message = data.get('message')
        user = self.scope['user']

        print("USER:", user)
        print("MESSAGE:", message)

        group = await self.get_group()
        print("GROUP FOUND:", group)

        msg = await self.create_message(group, user, message)
        print("MESSAGE SAVED:", msg)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
            }
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def get_group(self):
        return ChatGroup.objects.get(group_name=self.group_name)

    @database_sync_to_async
    def create_message(self, group, user, message):
        return GroupMessage.objects.create(
            group=group,
            author=user,
            body=message
        )
