from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_user
from django.contrib import messages


# Create your views here.

def home(response):
    if not response.user.is_authenticated:
        return redirect("login")

    return render(response, "main/home.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR, "Incorrect email or password.")
            return redirect("login")
        else:
            messages.add_message(request, messages.SUCCESS, "Successfully logged in.")
            login_user(request, user)
            return redirect("home")
    return render(request, "main/login.html")
