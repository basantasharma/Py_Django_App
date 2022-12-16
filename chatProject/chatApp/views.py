from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
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
    return render( request, 'index/index.html')


def register(request):
    return render(request, 'registration/newRegister.html')
def logIn(request):
    return render(request, 'login/login.html')
def logOut(request):
    logout(request)
    messages.info(request, "you have been successfully logged out")
    return redirect('home')
def startLogin(request):
    if request.method == "POST":
        userName = request.POST['userName']
        password = request.POST['password']
        user = authenticate(username=userName, password=password)
        if user is not None:
            login(request, user)
            fName = user.first_name
            messages.info(request, "you have been successfully logged In")
            return render(request, 'index/index.html', {"fName": userName})
        else:
            messages.error(request, "User Name or Password didn't matched.")
            return redirect('home')
    return redirect('home')
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
            messages.success(request, "You have been Registered please confirm email to login.")
            return redirect("login")
        else:
            messages.error(request, "Password and Confirm Password doesnot matched")
            return redirect("register")