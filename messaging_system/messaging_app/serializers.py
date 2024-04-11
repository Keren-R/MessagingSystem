from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for a User object.
    """
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for a Message object.
    """
    sender = serializers.SlugRelatedField(read_only=True, slug_field="username")
    receiver = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['created_at']
