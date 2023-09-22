from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.utils.safestring import mark_safe
from django.contrib import auth
from django.contrib import messages
import json
from .models import ChatRoom

def get_last_10_msgs(chat_id):
    chat = get_object_or_404(ChatRoom,id = chat_id)
    messages = chat.messages.order_by('-timestamp').all()[:8]
    return messages[::-1]

def index(request):

    user = request.user
    user_chats = ChatRoom.objects.filter(participants__user__username=user.username)
    context = {
        'user_chats': user_chats
    }
    return render(request, 'home.html', context)

@login_required
def rooms(request, room_id):
    user = request.user
    user_chats = ChatRoom.objects.filter(participants__user__username=user.username)

    chat = get_object_or_404(ChatRoom, pk=room_id)

    # Get the other participant's username
    other_user = chat.participants.exclude(user=user).first()
    print(other_user)

    return render(request, 'mainroom.html', {
        'room_id': mark_safe(json.dumps(room_id)),
        'username': mark_safe(json.dumps(request.user.username)),
        'user_chats': user_chats,
        'other_username': other_user,
    })

def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password :
            user = auth.authenticate(username=username , password=password)
            if user:
                auth.login(request,user)
                messages.success(request, 'You have been logged in successfully !!')
                return redirect('chat')
        else :
                messages.error(request, 'Username or password are incorrect !')
                return redirect('login')
    
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'تم تسجيل خروجك')
    return redirect('login')

    





