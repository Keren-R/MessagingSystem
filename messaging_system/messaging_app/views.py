from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer
from .utils import generate_error_object


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
                response_data = serializer.data
                response_status = status.HTTP_201_CREATED
            else:
                response_data = serializer.errors
                response_status = status.HTTP_400_BAD_REQUEST
        except User.DoesNotExist:
            error_msg = f"user named {user_name} does not exist."
            response_data, response_status = generate_error_object(error_type="not_found", error_msg=error_msg)

        return Response(response_data, status=response_status)


class MessageDetailView(APIView):
    """
    View for displaying and manipulate a single message.
    """
    def get(self, request, pk) -> Response:
        """
        Return the message object with the provided pk.
        """
        try:
            message = Message.objects.get(pk=pk)
            if request.user == message.sender or request.user == message.receiver:
                serializer = MessageSerializer(message)
                response_data = serializer.data
                response_status = status.HTTP_200_OK
            else:
                error_msg = "you are not authorised to retrieve this message"
                response_data, response_status = generate_error_object(error_type="not_authorised", error_msg=error_msg)
        except Message.DoesNotExist:
            error_msg = f"message with id {pk} does not exist."
            response_data, response_status = generate_error_object(error_type="not_found", error_msg=error_msg)

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
                error_msg = "you are not authorised to read this message"
                response_data, response_status = generate_error_object(error_type="not_authorised", error_msg=error_msg)

        except Message.DoesNotExist:
            error_msg = f"message with id {pk} does not exist."
            response_data, response_status = generate_error_object(error_type="not_found", error_msg=error_msg)

        return Response(data=response_data, status=response_status)

    def delete(self, request, pk):
        message = Message.objects.get(pk=pk)
        response_data = None

        if request.user == message.sender or request.user == message.receiver:
            message.delete()
            response_status = status.HTTP_204_NO_CONTENT
        else:
            error_msg = "you are not authorised to delete this message"
            response_data, response_status = generate_error_object(error_type="not_authorised", error_msg=error_msg)

        return Response(data=response_data, status=response_status)


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
