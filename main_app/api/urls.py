from django.urls import path, re_path

from .views import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView,


    MessageCreateView,
    MessageDetailView,
    MessageListView
)

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<pk>', ChatDetailView.as_view()),
    path('<pk>/update/', ChatUpdateView.as_view()),
    path('<pk>/delete/', ChatDeleteView.as_view()),


    path('msgs/', MessageListView.as_view()),
    path('msgs/<pk>', MessageDetailView.as_view()),
    path('msgs/create/', MessageCreateView.as_view()),
]