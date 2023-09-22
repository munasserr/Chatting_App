import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message,Contact,ChatRoom
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import get_last_10_msgs


class ChatConsumer(WebsocketConsumer):

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def fetch_messages(self, data):
        chat_id = data.get('chat_id')
        if chat_id is not None:
            messages = get_last_10_msgs(chat_id)
            content = {
                'command': 'messages',
                'messages': self.messages_to_json(messages),
            }
            self.send_chat_message(content)


    def new_message(self,data):
        author = data['from']
        author_user = Contact.objects.filter(user__username=author)[0]
        message = Message.objects.create(contact=author_user , content=data['message'])
        chat_room = ChatRoom.objects.get(id=data['chat_id'])
        if author_user in chat_room.participants.all():
            chat_room.messages.add(message)
            chat_room.save()
            content = {
                'command':'new_message',
                'message': self.message_to_json(message),
            }
            return self.send_chat_message(content)

    def message_to_json(self,message):
        return {
            'author': message.contact.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message
                }
        )


    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))