from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q
from django.utils.dateformat import DateFormat
from django.http import JsonResponse

# Create your views here.
@login_required
def ChatRoom(request, username):
    r = User.objects.filter(username = username).first()
    messages = Message.objects.filter(
        (Q(sender = request.user) & Q(receiver=r)) |
        (Q(sender = r) & Q(receiver= request.user))
    ).order_by("timestamp")

    if request.method == 'POST':
        msg = request.POST.get('msg')
        if msg:
            Message.objects.create(
                sender = request.user,
                receiver = r,
                content = msg
            )

    return render(request, "chat/chat.html",{"r":r, "messages":messages})

@login_required
def get_messages(request, username):
    r = User.objects.filter(username = username).first()

    messages = Message.objects.filter(
        (Q(sender = request.user) & Q(receiver=r)) |
        (Q(sender = r) & Q(receiver= request.user))
    ).order_by("timestamp")

    messages_data = [
        {
        "sender" : message.sender.username,
        "content" : message.content,
        "timestamp": DateFormat(message.timestamp).format('H:i')
        }
        for message in messages
    ]
    return JsonResponse({"messages":messages_data})