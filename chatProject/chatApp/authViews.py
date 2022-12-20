from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages




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
        
        return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponse('no such friend found')