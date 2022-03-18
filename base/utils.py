from django.shortcuts import redirect
from django.contrib import messages

from .models import TopicModel, RoomModel, MessageModel



def follow_user(request, user):
    user.followers.add(request.user)
    request.user.following.add(user)


def unfollow_user(request, user):
    user.followers.remove(request.user)
    request.user.following.remove(user)


def new_room(request):
        topic, created = TopicModel.objects.get_or_create(name=request.POST["topic"])

        RoomModel.objects.create(
        host=request.user,
        topic = topic,
        name = request.POST.get("room_name"),
        description= request.POST.get("room_about")
        ) 

def create_room_message(request, room,):
    message_body = request.POST.get("body")

    try:
        MessageModel.objects.create(
            user=request.user,
            room=room,
            body=message_body
            )
        room.participant.add(request.user)

    except Exception as e:
        messages.error("and error as occured while trying to create a message")

