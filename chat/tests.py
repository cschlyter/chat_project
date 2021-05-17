from django.test import TestCase

from chat.models import Room
from chat.services import MessageService


class MessageServiceTestCase(TestCase):

    def setUp(self):
        service = MessageService()
        self.service = service

    def test_insert_message_for_existing_room(self):
        """ Test Message insertion code """

        room_name = "Room1"

        r = Room(name=room_name)
        r.save()

        message = "Hello"
        user = "User 1"

        m = self.service.insert_message(room_name, message, user)

        self.assertEqual(m.room.name, room_name)
        self.assertEqual(m.message, message)
        self.assertEqual(m.user, user)

    def test_insert_message_for_non_existing_room(self):
        """ Test Message insertion code """

        room_name = "Room1"
        message = "Hello"
        user = "User 1"

        with self.assertRaises(Room.DoesNotExist):
            self.service.insert_message(room_name, message, user)
