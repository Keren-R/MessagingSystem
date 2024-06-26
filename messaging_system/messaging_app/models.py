from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    """
    Model of a Message object.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False)

