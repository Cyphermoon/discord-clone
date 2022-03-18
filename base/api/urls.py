from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.getRoutes), 
    path("room-messages/", views.get_room_messages),
    path("create-room-message/", views.create_room_message_api)
]