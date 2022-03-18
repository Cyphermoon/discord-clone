from rest_framework.serializers import ModelSerializer
from base.models import RoomModel, MessageModel, User


class RoomSerializer(ModelSerializer):
    class Meta:
        model = RoomModel
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    class Meta:
        model = MessageModel
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]