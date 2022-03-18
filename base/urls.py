from django.urls import path

from . import views

urlpatterns = [ 
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("register/", views.register, name="register"),



    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room_item, name="room"),
    path("topics/", views.topicPage, name="topics"),
    path('profile/<str:pk>/', views.profile, name="profile" ),
    path('profile/<str:pk>/followers/', views.user_followers_page, name="user_followers" ),
    path('profile/<str:pk>/followings/', views.user_following_page, name="user_following" ),


    path("update_profile/", views.update_profile, name="update_profile"),
    
    path('create_room/', views.create_room, name="create_room"),
    path('update_room/<str:pk>/', views.update_room, name="update_room"),
    path('delete_room/<str:pk>/', views.delete_room, name="delete_room"),
    path('delete_message/<str:pk>', views.delete_message, name="delete_message")
]