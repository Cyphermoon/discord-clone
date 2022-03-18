from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import RoomModel, User



class RoomForm(ModelForm):
    class Meta:
        model = RoomModel
        fields = "__all__"
        exclude = ["host", "participant"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "name", "email", "bio"]


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "name", "email","password1", "password2", "bio"]
