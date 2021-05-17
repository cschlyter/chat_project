import json
import requests
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer

from chat.models import Room, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        if message != "" and message[0] == "/":
            async_to_sync(self.channel_layer.send)('background-tasks', {
                'type': 'stock',
                'command': message,
                'room_group_name': self.room_group_name
            })
        else:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']

        room = Room.objects.get(name=self.room_name)

        m = Message(room=room, message=message, user=user)
        m.save()

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'date': m.formatted_timestamp
        }))


class BackgroundTaskConsumer(SyncConsumer):

    def stock(self, message):
        command = message.get("command")
        room_group_name = message.get("room_group_name")
        channel_layer = get_channel_layer()
        user = "Stock Robot"

        if command.startswith("/stock="):

            stock_name = command.split("=")[1]

            url = f"https://stooq.com/q/l/?s={stock_name.lower()}&f=sd2t2ohlcv&h&e=csv"

            r = requests.get(url)
            csv_file = r.content
            data = csv_file.decode('utf-8').splitlines()
            share_open_value = data[1].split(",")[3]
            robot_message = f"{stock_name.upper()} quote is {share_open_value} per share"

            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'chat_message',
                    'message': robot_message,
                    'user': user
                }
            )
        else:
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'chat_message',
                    'message': f"Invalid command: {command}. Try /stock=STOCK_NAME",
                    'user': user
                }
            )


