from chat.models import Room, Message


class MessageService:

    @staticmethod
    def insert_message(room_name, message, user):
        room = Room.objects.get(name=room_name)

        m = Message(room=room, message=message, user=user)
        m.save()

        return m
