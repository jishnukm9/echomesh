
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"{self.room_name}"

        print(f"WebSocket connected to room {self.room_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print(f"WebSocket disconnected from room {self.room_name}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userid = text_data_json['userid']
        image = text_data_json['image']
        fullname = text_data_json['fullname']
        roomname=text_data_json['roomname']
        # print("message-recieve",message)
        # Send message to room group

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                "userid":userid,
                "image":image,
                "fullname":fullname,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        userid = event['userid']
        image = event['image']
        fullname = event['fullname']
        print("message- from chat medssage",message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
             "userid":userid,
                "image":image,
                "fullname":fullname,
        }))





class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"{self.room_name}"

        print(f"WebSocket connected to room {self.room_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print(f"WebSocket disconnected from room {self.room_name}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification_message',
                'message': message,
            }
        )

    async def notification_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
        }))



