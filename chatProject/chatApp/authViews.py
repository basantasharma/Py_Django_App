from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection, models
from django.db.models import Case, Count, Q, When
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import user_friend_requests


@login_required
def logOut(request):
    logout(request)
    messages.info(request, "you have been successfully logged out")
    return redirect("home")


@login_required
def addFriend(request):
    redirect_url = request.META.get("HTTP_REFERER", "/")
    friend_id = request.GET["id"]
    try:
        friend = User.objects.get(id=friend_id)
    except User.DoesNotExist:
        friend = None
    if friend is not None:
        request_save = user_friend_requests(
            from_users_id=request.user.id, to_users_id=friend_id
        )
        request_save.save()
        return HttpResponseRedirect(redirect_url)
    else:
        messages.error(request, "No such friend found")
        return redirect("/")  # HttpResponseRedirect(redirect_url)


@login_required
def seeRecievedRequests(request):
    request_sent_by_others = requestSentByOthers(request)
    return render(
        request,
        "friend/request.html",
        {
            "request_sent_by_others": request_sent_by_others,
        },
    )


@login_required
def seeSentRequests(request):
    request_sent_by_you = requestSentByYou(request)
    return render(
        request,
        "friend/request.html",
        {
            "request_sent_by_you": request_sent_by_you,
        },
    )


def requestSentByOthers(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_user.id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, user_friend_requests.is_accepted FROM auth_user INNER JOIN user_friend_requests ON user_friend_requests.to_users_id = %s AND user_friend_requests.from_users_id = auth_user.id AND auth_user.username != 'admin' AND user_friend_requests.is_accepted = 0",
            [request.user.id],
        )
        return cursor.fetchall()


def requestSentByYou(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_user.id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, user_friend_requests.is_accepted FROM auth_user INNER JOIN user_friend_requests ON user_friend_requests.to_users_id = auth_user.id AND user_friend_requests.from_users_id = %s AND auth_user.username != 'admin' AND user_friend_requests.is_accepted = 0",
            [request.user.id],
        )
        return cursor.fetchall()


def request_sent_by_user(request, of_user):
    return user_friend_requests.objects.filter(
        Q(to_users_id=of_user) & Q(from_users_id=request.user.id)
    )


def request_sent_to_user(request, of_user):
    return user_friend_requests.objects.filter(
        Q(to_users_id=request.user.id) & Q(from_users_id=of_user)
    )


@login_required
def seeFriend(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT auth_user.id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, user_friend_requests.is_accepted FROM auth_user INNER JOIN user_friend_requests ON user_friend_requests.to_users_id IN (auth_user.id, %s) AND user_friend_requests.from_users_id IN (%s, auth_user.id) AND auth_user.username != 'admin' AND user_friend_requests.is_accepted = 1",
            [request.user.id, request.user.id],
        )
        friends = cursor.fetchall()
    return render(
        request,
        "friend/seeFriend.html",
        {
            "friends": friends,
        },
    )


@login_required
def unFriend(request):
    redirect_url = request.META.get("HTTP_REFERER", "/")
    of_user = request.GET["id"]
    if request_sent_to_user(request, of_user):
        user_friend_requests.objects.filter(
            Q(to_users_id=request.user.id) & Q(from_users_id=of_user)
        ).update(is_accepted=0)
    else:
        messages.error(request, "no request found")
    return HttpResponseRedirect(redirect_url)


@login_required
def cancleRequest(request):
    redirect_url = request.META.get("HTTP_REFERER", "/")
    of_user = request.GET["id"]
    if request_sent_by_user(request, of_user):
        user_friend_requests.objects.filter(
            Q(to_users_id=of_user) & Q(from_users_id=request.user.id)
        ).delete()
    else:
        messages.error(request, "no request found")
    return HttpResponseRedirect(redirect_url)


@login_required
def acceptRequest(request):
    redirect_url = request.META.get("HTTP_REFERER", "/")
    of_user = request.GET["id"]
    if request_sent_to_user(request, of_user):
        user_friend_requests.objects.filter(
            Q(to_users_id=request.user.id) & Q(from_users_id=of_user)
        ).update(is_accepted=1)
    return HttpResponseRedirect(redirect_url)


@login_required
def viewProfile(request):
    redirect_url = request.META.get("HTTP_REFERER", "/")
    user_id = request.GET["q"]
    user_result = (
        User.objects.values("id", "username", "first_name", "last_name", "email")
        .filter(Q(id=user_id))
        .exclude(username="admin")
    )
    # print(user_result[0]['id'])
    # is_friend = user_friend_requests.objects.filter(Q(to_users_id__in = (request.user.id, user_id)) & Q(from_users_id__in = (request.user.id, user_id)) & Q(is_accepted = 1))
    # requestSentByUser = user_friend_requests.objects.filter(Q(to_users_id = user_id) & Q(from_users_id = request.user.id) & Q(is_accepted = 0))
    # requestSentByOther = user_friend_requests.objects.filter(Q(to_users_id = request.user.id) & Q(from_users_id =  user_id) & Q(is_accepted = 0))
    if user_friend_requests.objects.filter(
        Q(to_users_id__in=(request.user.id, user_id))
        & Q(from_users_id__in=(request.user.id, user_id))
        & Q(is_accepted=1)
    ):
        status = 1.1
    elif user_friend_requests.objects.filter(
        Q(to_users_id=user_id) & Q(from_users_id=request.user.id) & Q(is_accepted=0)
    ):
        status = 1.0
    elif user_friend_requests.objects.filter(
        Q(to_users_id=request.user.id) & Q(from_users_id=user_id) & Q(is_accepted=0)
    ):
        status = 0.1
    else:
        status = 0.0

    return render(
        request, "profile/profile.html", {"results": user_result, "status": status}
    )
