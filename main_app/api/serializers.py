from rest_framework import serializers
from ..models import ChatRoom,Contact,Message


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        # Convert the provided username to a Contact object
        contact = Contact.objects.get(user__username=value)
        return contact
    



class ChatRoomSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'messages', 'participants']
        read_only = ['id']

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = ChatRoom()
        chat.save()
        for username in participants:
            contact = Contact.objects.filter(user__username=username)[0]
            chat.participants.add(contact)
        chat.save()
        return chat
    

class MessagesSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(write_only=True)
    chat_room_id = serializers.IntegerField(write_only=True)  # Add this field for chat room ID

    class Meta:
        model = Message
        fields = ['id', 'content', 'contact', 'chat_room_id']
        read_only_fields = ['id']

    def create(self, validated_data):
        contact_username = validated_data.pop('contact', None)
        chat_room_id = validated_data.pop('chat_room_id', None)  # Retrieve chat room ID

        if contact_username:
            try:
                contact = Contact.objects.get(user__username=contact_username)
            except Contact.DoesNotExist:
                raise serializers.ValidationError("Contact with this username does not exist.")
            validated_data['contact'] = contact

        message = Message.objects.create(**validated_data)

        if chat_room_id:
            try:
                chat_room = ChatRoom.objects.get(pk=chat_room_id)
                chat_room.messages.add(message)  # Add the message to the chat room
            except ChatRoom.DoesNotExist:
                raise serializers.ValidationError("Chat room with this ID does not exist.")

        return message

