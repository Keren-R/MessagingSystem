from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer


class MessagesList(APIView):
    """
    View to list all messages.
    """
    def get(self, request, format=None):
        """
        Return a list of all sent or received messages by the logged-in user.
        """
        user = self.request.user
        messages = Message.objects.filter(Q(sender_id=user) | Q(receiver_id=user))
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new message instance.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            user_name = request.data.get('receiver')
            receiver = User.objects.get(username=user_name)
            serializer.save(sender=request.user, receiver=receiver)
            data = serializer.data
            response_status = status.HTTP_201_CREATED
        else:
            data = serializer.errors
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(data, status=response_status)


class MessageDetailView(APIView):
    """
    View for displaying and manipulate a single message.
    """
    def get(self, request, pk):
        """
        Return the message object with the provided pk.
        """
        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message)
            data = serializer.data
            response_status = status.HTTP_200_OK
        except Message.DoesNotExist:
            data = None
            response_status = status.HTTP_404_NOT_FOUND

        return Response(data=data, status=response_status)

    def put(self, request, pk):
        try:
            message = Message.objects.get(pk=pk)
            message.is_read = True
            message.save()
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        message = Message.objects.get(pk=pk)

        if request.user == message.sender or request.user == message.receiver:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You are not authorized to delete this message."},
                            status=status.HTTP_403_FORBIDDEN)


class UnreadMessagesList(APIView):
    """
    View to list all unread messages.
    """
    def get(self, request, format=None):
        """
        Return a list of all unread messages.
        """
        messages = Message.objects.filter(receiver=self.request.user, is_read=False)
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)
