from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import user_friend_requests




from django.db import connection
from django.db.models import Q



def logOut(request):
    logout(request)
    messages.info(request, "you have been successfully logged out")
    return redirect('home')

def addFriend(request):
    redirect_url = request.META.get('HTTP_REFERER', 'home')
    friend_id = request.GET['id']
    try:
        friend = User.objects.get(id = friend_id)
    except User.DoesNotExist:
        friend = None
    if friend is not None:
        request_save = user_friend_requests(from_users_id = request.user.id, to_users_id = friend_id)
        request_save.save()
        return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponse('no such friend found')

def seeFriend(request):
    result = user_friend_requests.objects.all().values("from_users_id", "to_users_id", "is_accepted").filter(from_users_id = request.user.id)
    return HttpResponse(result)