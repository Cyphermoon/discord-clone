from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email=models.EmailField(max_length=255, unique=True, null=True)
    bio = models.TextField(null=True)
    followers = models.ManyToManyField('User', blank=True)
    following = models.ManyToManyField('User', related_name="people_following", blank=True)


    REQUIRED_FIELDS = []

    avatar = CloudinaryField('image', default='avatar.svg')

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    


class TopicModel(TimeStampModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RoomModel(TimeStampModel):
    host = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(TopicModel,on_delete=models.SET_NULL, null=True)
    name= models.CharField(max_length=255)
    participant=models.ManyToManyField(User, related_name="participant")
    description = models.TextField(null=True, blank=True)


    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-created", "-updated"]



class MessageModel(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    replied_msg = models.ForeignKey("MessageModel", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.body[:50]


