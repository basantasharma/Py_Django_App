"""chatProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.urls import path
from chatApp import authViews, views
from django.contrib import admin
from django.urls import path, include

# from chatApp.views import ShowIndex
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.showIndex, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.logIn, name="login"),
    path("logout/", authViews.logOut, name="logout"),
    path("startLogin/", views.startLogin, name="startLogin"),
    path("startRegistration/", views.startRegistration, name="startRegistration"),
    path("search/", views.search, name="search"),
    path("addFriend/", authViews.addFriend, name="addFriend"),
    path("friends/", authViews.seeFriend, name="addFriend"),
    path("unFriend/", authViews.unFriend, name="unFriend"),
    path("cancleRequest/", authViews.cancleRequest, name="cancleRequest"),
    path("acceptRequest/", authViews.acceptRequest, name="acceptRequest"),
    path("profile/", authViews.viewProfile, name="profile"),
    path("sentRequestes/", authViews.seeSentRequests, name="sentRequestes"),
    path("recievedRequestes/", authViews.seeRecievedRequests, name="recievedRequestes"),
    path("chat/", authViews.chat, name="chat"),
    path("chat/<str:room_name>/", authViews.room, name="room"),
    #path("ws/sc/", include('chatApp.urlsWebsocket')),
]
