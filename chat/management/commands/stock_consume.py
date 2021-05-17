import pika
import json
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.management.base import BaseCommand

from chat.models import Room, Message


class Command(BaseCommand):
    help = 'Consumes a rabbitmq queue with stock quotes from the Stock Bot'

    def handle(self, *args, **options):
        print(settings.RABBIT_HOST)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST))
        channel = connection.channel()

        channel.queue_declare(queue='stock_queue')

        def callback(ch, method, properties, body):
            message = json.loads(body)

            room_name = message.get("room")
            room = Room.objects.get(name=room_name)

            m = Message(room=room, message=message.get("message"), user=message.get("user"))
            m.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'chat_' + room_name,
                {
                    'type': 'chat_message',
                    'message': m.message,
                    'user': m.user,
                    'date': m.formatted_timestamp
                }
            )

        channel.basic_consume(queue='stock_queue', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
