from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):

    user = models.ForeignKey(User,related_name='friends',on_delete=models.CASCADE)
    friends = models.ManyToManyField('self',blank = True)

    def __str__(self):
        return self.user.username

class Message(models.Model):

    contact = models.ForeignKey(Contact,related_name='messages',on_delete=models.CASCADE)
    content = models.TextField(max_length=750)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def last_10_messages():
    #     messages = Message.objects.all().order_by('-timestamp')[:10]
    #     return messages[::-1]

    def __str__(self):
        return self.contact.user.username
    
class ChatRoom(models.Model):

    participants = models.ManyToManyField(Contact,related_name='chats',)
    messages = models.ManyToManyField(Message,blank=True)

    # def last_10_messages(self):
    #     messages = self.messages.all().order_by('-timestamp')[:10]
    #     return messages[::-1]
    
    def __str__(self):
        return str(self.pk)



    



