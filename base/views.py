from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import RoomModel, TopicModel, MessageModel, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from .utils import follow_user, unfollow_user, new_room, create_room_message


# Create your views here.

# rooms = [
#     {"id":1, "name":"Let us learn js"},
#     {"id":2, "name":"The future is now"},
#     {"id":3, "name":"I am you best option"},
# ]


def login_page(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        
        except:
            messages.error(request, "This user is not present")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "username or password is incorrect ")

    context = {
        "page":page
    }
    return render(request, "base/login.html", context)


def logout_page(request):
    logout(request)
    return redirect("home")


def register(request):
    register_form = MyUserCreationForm()

    if request.method == "POST":
        register_form = MyUserCreationForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "an error occurred during registration")

    context = {
        "register_form":register_form
    }

    return render(request, "base/register.html", context)


def home(request):
    search_query = request.GET.get("q", "") 


    rooms = RoomModel.objects.filter(Q(topic__name__icontains = search_query) 
                                    | Q(name__icontains = search_query) | 
                                    Q(description__icontains = search_query) | 
                                    Q(host__username__icontains = search_query)  )

    topics = TopicModel.objects.all()
    room_count = rooms.count()
    recent_messages = MessageModel.objects.filter(room__topic__name__icontains=search_query).order_by("-created")[:10]

    context = {
        "rooms":rooms,
        "room_count":room_count,
        "topics":topics,
        "recent_messages":recent_messages
        }

    return render(request, 'base/index.html', context)


@login_required(login_url="/login")
def room_item(request, pk):
    room = RoomModel.objects.get(id=pk)
    room_messages = room.messagemodel_set.all()
    participants = room.participant.all()
    

    if request.method == "POST":
        create_room_message(request, room)
        return redirect("room", pk=room.id)

    context = {
        "room":room,
        "room_messages": room_messages,
        "participants":participants
    }

    return render(request, "base/room.html", context)


@login_required(login_url="/login")
def create_room(request):
    room_form = RoomForm()
    topics = TopicModel.objects.all()
    form_page = "create"

    if request.method == "POST":
        new_room(request)

        return redirect("home")

            
        # room_form = RoomForm(request.POST)
        # if room_form.is_valid():
        #     room = room_form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect("home")

        # else:
        #     assert False

    context = {
        "room_form":room_form,
        "topics":topics,
        "form_page":form_page
    }

    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def update_room(request, pk):
    room = RoomModel.objects.get(id=pk)
    form_page = "update"

    if request.user.username != room.host.username:
        return HttpResponse("you do not belong here")

    room_form = RoomForm(instance=room)

    if request.method == "POST":
        room_form = RoomForm(request.POST, instance=room)
        if room_form.is_valid():
            room_form.save()
            return redirect("home")

    context = {
        "room_form":room_form,
        "form_page":form_page
    }

    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def delete_room(request, pk):
    room = RoomModel.objects.get(id=pk)

    if request.user.username != room.host.username:
        return HttpResponse("you do not belong here")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    context = {
        "obj":room
    }

    return render(request, "base/delete_room.html", context)



@login_required(login_url="/login")
def delete_message(request, pk):
    room_message = MessageModel.objects.get(id=pk)

    if request.user.username != room_message.user.username:
        return HttpResponse("you do not belong here")

    if request.method == "POST":
        room_message.delete()
        return redirect("home")

    context = {
        "obj":room_message,
    }

    return render(request, "base/delete_room.html", context)

@login_required(login_url="/login")
def profile(request, pk):

    topics = TopicModel.objects.all()
    user = User.objects.get(id=pk)
    user_followers= user.followers.all()
    user_followings= user.following.all()
    rooms= user.roommodel_set.all()
    recent_messages= user.messagemodel_set.all()


    if request.method == 'POST' and request.user != user:
       
        if request.POST.get("action") == "follow":
           follow_user(request, user)
        
        if request.POST.get("action") == "unfollow":
            unfollow_user(request, user)

    context = {
        "user":user,
        "topics":topics,
        "recent_messages":recent_messages,
        "rooms":rooms,
        "user_followers":user_followers,
        "user_followings":user_followings
    }

    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def update_profile(request):
    user = User.objects.get(id=request.user.id)
    user_form = UserForm(instance=user)

    if request.method == "POST":
        user_form=UserForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            return redirect("home")

        else:
            assert False

    context = {
        "user":user,
        "user_form":user_form
    }

    return render(request, "base/update_profile.html", context)


def topicPage(request):
    search_query = request.GET.get("q", "")
    topics = TopicModel.objects.filter(name__icontains=search_query)

    context = {
        "topics":topics
    }

    return render(request, "base/topics.html", context)


def user_followers_page(request, pk):
    page = "followers_page"
    user = User.objects.get(id=pk)
    user_followers= user.followers.all()

    context = {
        "follows":user_followers,
        "user":user,
        "page":page
    }

    return render(request, "base/follow.html", context)



def user_following_page(request, pk):
    page = "follow_page"

    user = User.objects.get(id=pk)
    user_following= user.following.all()

    context = {
        "follows":user_following,
        "user":user,
        "page":page

    }

    return render(request, "base/follow.html", context)