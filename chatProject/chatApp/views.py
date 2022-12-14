from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.db.models import Q, Sum, Count, Case, Value, When, IntegerField
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

# from .models import registrationForm
# from django.views.generic.list import ListView
# from .forms import registrationForms

# Create your views here.
def showIndex(request):
    # if request.method == 'POST':
    #     fn = registrationForms(request.POST)
    #     if fn.is_valid():
    #         firstName = fn.cleaned_data['firstName']
    #         lastName = fn.cleaned_data['lastName']
    # else:
    #     fn = registrationForms()
    return render(request, "index/index.html")


def register(request):
    return render(request, "registration/newRegister.html")


def logIn(request):
    return render(request, "login/login.html")


# CSRF verification failed. Request aborted. need to be handled cuz login paachi back gayera pheri login gare error xa
def startLogin(request):
    redirect_url = request.META.get("HTTP_REFERER", "/")
    # request.GET.get('next', '/')
    if request.method == "POST":
        userName = request.POST["userName"]
        password = request.POST["password"]
        user = authenticate(username=userName, password=password)
        if user is not None:
            login(request, user)
            # fName = user.first_name
            messages.info(request, "you have been successfully logged In")
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect(
                    "home"
                )  # render(request, 'index/index.html', {"fName": fName})
        else:
            messages.error(request, "Username or Password didn't matched.")
            return redirect(redirect_url)
    else:
        # messages.error(request, "need to login to access this page")
        return redirect("home")


def startRegistration(request):
    if request.method == "POST":
        userName = request.POST["userName"]
        fName = request.POST["fName"]
        lName = request.POST["lName"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmPassword = request.POST["cPassword"]
        if password == confirmPassword:
            myUser = User.objects.create_user(userName, email, password)
            myUser.first_name = fName
            myUser.last_name = lName
            myUser.save()
            messages.success(
                request, "You have been Registered please confirm email to login."
            )
            return redirect("login")
        else:
            messages.error(request, "Password and Confirm Password doesnot matched")
            return redirect("register")


def search(request):

    search_for = request.GET["q"]
    search_result = findUser(request, search_for)
    return render(
        request,
        "search/search.html",
        {
            "searched_for": search_for,
            "results": search_result,
        },
    )


def findUser(request, search_for):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT auth_user.id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, user_friend_requests.is_accepted FROM auth_user INNER JOIN user_friend_requests ON auth_user.username LIKE '%%s%' OR  auth_user.email LIKE '%%s%' ")
    return (
        User.objects.all()
        .values("id", "username", "first_name", "last_name", "email")
        .filter(Q(username__contains=search_for) | Q(email__contains=search_for))
        .exclude(Q(username="admin") | Q(id=request.user.id))
    )
