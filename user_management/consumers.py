import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from user_management import models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.sender = self.scope['user']

        if not self.sender.is_authenticated:
            await self.close()

        # Construct room group name based on both users
        self.room_group_name = f'chat_{min(self.sender.id, int(self.receiver_id))}_{max(self.sender.id, int(self.receiver_id))}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send previous messages to the receiver when they connect
        messages = Message.objects.filter(
            (models.Q(sender=self.sender, receiver=self.receiver) | models.Q(sender=self.receiver, receiver=self.sender))
        ).order_by('timestamp')

        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.message,
                'sender': message.sender.username,
                'timestamp': message.timestamp.isoformat(),
            }))

    async def disconnect(self, close_code):
        # Leave room group on disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send the message to the database
        receiver = User.objects.get(id=self.receiver_id)
        message_obj = Message.objects.create(
            sender=self.sender,
            receiver=receiver,
            message=message
        )

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_obj.message,
                'sender': self.sender.username,
                'timestamp': message_obj.timestamp.isoformat(),
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))