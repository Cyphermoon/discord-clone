from datetime import datetime
import datetime as d

from django.urls import reverse
from django.utils.timesince import timesince

from .serializer import UserSerializer
from base.models import MessageModel



def get_replied_msg(replied_msg_id):
    replied_msg_obj = None

    if replied_msg_id is not None:
        replied_msg_obj = MessageModel.objects.get(id = replied_msg_id)

    return replied_msg_obj


def get_particpant(message_obj):
        participant_list =  message_obj.room.participant.all()
        user_serializer = UserSerializer(participant_list, many=True)
        return user_serializer.data


def build_res_data(replied_msg_obj, message_obj,id, body):
    res_data = {}

    if replied_msg_obj is not None:
        res_data["replied_msg"] = replied_msg_obj.body
        res_data["replied_user"] = replied_msg_obj.user.username
        
    res_data["message_id"] = id
    res_data["username"] = message_obj.user.username
    res_data["body"] = body
    res_data["user_url"] = reverse("profile", kwargs={"pk": message_obj.user.id})
    res_data["timesince"] = timesince(message_obj.created, now=datetime.now().replace(tzinfo=d.timezone.utc))
    res_data["delete_url"] = reverse("delete_message", kwargs={"pk": id})
    res_data["participants_list"] = get_particpant(message_obj)

    return res_data