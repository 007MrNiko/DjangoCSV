from django.shortcuts import render, redirect

# Create your views here.

def home(response):
    return render(response, "main/home.html")
