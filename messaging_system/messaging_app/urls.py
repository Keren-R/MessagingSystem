from django.urls import path, include
from django.views.generic import RedirectView

from .views import MessagesList, MessageDetailView, UnreadMessagesList

urlpatterns = [
    path('messages/', MessagesList.as_view(), name='messages-list'),
    path('messages/<int:pk>', MessageDetailView.as_view()),
    path('unread/', UnreadMessagesList.as_view()),
    path('', RedirectView.as_view(url='/messages/', permanent=True))
]
