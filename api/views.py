from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import RoomSerializer
from base.models import RoomModel



@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /api/rooms", 
        "GET /api/rooms/:id"
    ]

    return Response(routes)


@api_view(["GET"])
def getRooms(request):
    rooms = RoomModel.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)



@api_view(["GET"])
def getRoom(request, pk):
    rooms = RoomModel.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)


