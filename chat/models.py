from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    user = models.CharField(max_length=150)
    timestamp = models.DateTimeField(default=datetime.now, db_index=True)

    def __str__(self):
        return self.user + ": " + self.message

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
