from django.urls import path, include

from .views import MessagesList, MessageDetailView, UnreadMessagesList

urlpatterns = [
    path('messages/', MessagesList.as_view(), name='messages-list'),
    path('messages/<int:pk>', MessageDetailView.as_view()),
    path('unread/', UnreadMessagesList.as_view())
    # path('users/', UsersList.as_view(), name='users-list'),
]
