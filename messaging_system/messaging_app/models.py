from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     name = models.CharField(max_length=100)
#     password = models.CharField(max_length=20)
#     login = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False)

