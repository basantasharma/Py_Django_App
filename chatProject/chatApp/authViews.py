from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import user_friend_requests




from django.db import connection, models
from django.db.models import Q, Count, Case, When



def logOut(request):
    logout(request)
    messages.info(request, "you have been successfully logged out")
    return redirect('home')

def addFriend(request):
    redirect_url = request.META.get('HTTP_REFERER', '/home')
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
    with connection.cursor() as cursor:
        cursor.execute("Select auth_user.id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, user_friend_requests.is_accepted FROM auth_user INNER JOIN user_friend_requests ON user_friend_requests.to_users_id = auth_user.id AND user_friend_requests.from_users_id = %s AND auth_user.username != 'admin'", [request.user.id])   # WHERE auth_user.id IN (SELECT fr.to_users_id FROM user_friend_requests AS fr WHERE from_users_id = %s)", [request.user.id])
        rows = cursor.fetchall()
    return render(request, 'friend/seeFriend.html', {
        'friends': rows
    })

# def seeFriend(request):
#     # friends = User.objects.select_related('user_friend_requests').filter(from_users_id = request.user.id)
#     # friends = User.objects.all().values('id', 'username','first_name', 'last_name', 'email').filter(
#     #     id__in=user_friend_requests.objects.filter(from_users_id= request.user.id).values('to_users_id')
#     # ).exclude(username= 'admin')
#     return render(request, 'friend/seeFriend.html', {
#         'friends': friends
#     })
    #return HttpResponse(friends)

def cancleRequest(request):
    redirect_url = request.META.get('HTTP_REFERER', '/home')
    of_user = request.GET['id']
    result = user_friend_requests.objects.filter(Q(to_users_id = of_user) & Q(from_users_id = request.user.id)).delete()
    #return HttpResponse(result)
    return HttpResponseRedirect(redirect_url)