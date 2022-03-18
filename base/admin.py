from django.contrib import admin

from .models import TopicModel, MessageModel, RoomModel, User

# Register your models here.

admin.site.register(User)
admin.site.register(TopicModel)
admin.site.register(RoomModel)
admin.site.register(MessageModel)

