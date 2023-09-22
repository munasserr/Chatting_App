from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
) 
from ..models import ChatRoom,Contact,User,Message
from .serializers import ChatRoomSerializer,MessagesSerializer

def get_user_contact(username):
    user = get_object_or_404(User ,username=username)
    contact = get_object_or_404(Contact ,user=user)
    return contact

class ChatListView(ListAPIView):

    def get_queryset(self):
        queryset = ChatRoom.objects.all()
        username = self.request.query_params.get('username',None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset
    
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.AllowAny]

class ChatDetailView(RetrieveAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.AllowAny]

class ChatCreateView(CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatUpdateView(UpdateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated, )



#------------------------- Messages Views --------------------------------

class MessageListView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [permissions.AllowAny]

class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = (permissions.IsAuthenticated, )

class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def perform_create(self, serializer):
        # Get the 'chat_room_id' from the request data
        chat_room_id = self.request.data.get('chat_room_id')

        serializer.save(chat_room_id=chat_room_id)  # Pass the 'chat_room_id' to the serializer




