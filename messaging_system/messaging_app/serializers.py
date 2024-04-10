from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    # sender_details = serializers.CharField(source='sender.name')
    # receiver_details = serializers.RelatedField(source='name', read_only=True)

    sender = serializers.SlugRelatedField(read_only=True, slug_field="username")
    receiver = serializers.SlugRelatedField(read_only=True, slug_field="username")
    # sender = UserSerializer()
    # receiver = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['created_at']
