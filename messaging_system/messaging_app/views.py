from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer


class MessagesList(APIView):
    """
    View to list all messages.
    """
    def get(self, request):
        """
        Return a list of all sent or received messages by the logged-in user.
        """
        user = self.request.user
        messages = user.sent_messages.all() | user.received_messages.all()
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)

    def post(self, request) -> Response:
        """
        Create a new message instance.
        """
        serializer = MessageSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user_name = request.data.get('receiver')
                receiver = User.objects.get(username=user_name)
                serializer.save(sender=request.user, receiver=receiver)
                data = serializer.data
                response_status = status.HTTP_201_CREATED
            else:
                data = serializer.errors
                response_status = status.HTTP_400_BAD_REQUEST
        except User.DoesNotExist:
            response_status = status.HTTP_404_NOT_FOUND
            data = {"error": f"user named {user_name} does not exist."}

        return Response(data, status=response_status)


class MessageDetailView(APIView):
    """
    View for displaying and manipulate a single message.
    """
    def get(self, request, pk) -> Response:
        """
        Return the message object with the provided pk.
        """
        response_data = None
        try:
            message = Message.objects.get(pk=pk)
            if request.user == message.sender or request.user == message.receiver:
                serializer = MessageSerializer(message)
                response_data = serializer.data
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_403_FORBIDDEN
                response_data = {"error": "you are not authorised to retrieve this message"}
        except Message.DoesNotExist:
            response_status = status.HTTP_404_NOT_FOUND
            response_data = {"error": f"message with id {pk} does not exist."}

        return Response(data=response_data, status=response_status)

    def put(self, request, pk) -> Response:
        try:
            reader = request.user
            message = Message.objects.get(pk=pk)
            if reader == message.receiver:
                message.is_read = True
                message.save()
                serializer = MessageSerializer(message)
                response_data = serializer.data
                response_status = status.HTTP_200_OK
            else:
                response_data = {"error": "you are not authorised to read this message"}
                response_status = status.HTTP_403_FORBIDDEN
        except Message.DoesNotExist:
            response_data = {}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(data=response_data, status=response_status)

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
    def get(self, request) -> Response:
        """
        Return a list of all unread messages.
        """
        messages = Message.objects.filter(receiver=self.request.user, is_read=False)
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)
