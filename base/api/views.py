from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import RoomSerializer, MessageSerializer, UserSerializer
from base.models import RoomModel, MessageModel

from .utils import get_replied_msg, build_res_data


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /base/api/room-messages", 
        "POST /base/api/createroom-messages"
    ]

    return Response(routes)


@api_view(["GET"])
def get_room_messages(request):
    rooms = RoomModel.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_room_message_api(request):
    serializer = MessageSerializer(data=request.data)
  
    if serializer.is_valid():
        replied_msg_id = request.data.get("replied_msg_id")
        replied_msg_obj = get_replied_msg(replied_msg_id)
        
        serializer.save(replied_msg = replied_msg_obj)

        id = serializer.data.get("id")
        body = serializer.data.get("body")
        message_obj = MessageModel.objects.get(id = int(id))   

        res_data = build_res_data(replied_msg_obj,message_obj, id, body)

        message_obj.room.participant.add(request.user)

        return Response(res_data)
        
    return Response(serializer.errors)





