from django.db import models
from django.contrib.auth import get_user_model

from myprofile.models import Profile

class Message(models.Model):
    author = models.ForeignKey(get_user_model(), related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    roomName = models.IntegerField()

    def __str__(self):
        return self.author.name

    def last_10_messages(room):
        return Message.objects.order_by('timestamp').filter(roomName=room)

class MessageGroup(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='Message_1', on_delete=models.CASCADE)
    friend = models.ForeignKey(
        get_user_model(), related_name='Message_2', on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user.name