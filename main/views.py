from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login as login_user,
    logout as logout_user
)
from django.contrib import messages

from main.models import Schemas
from main.forms import SchemasNewForm


# Create your views here.

def home(response):
    if not response.user.is_authenticated:
        return redirect("login")

    return render(response, "main/home.html")


def schemas(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user_schemas = Schemas.objects.all().filter(user=request.user)

    data = {
        "schemas": user_schemas
    }

    return render(request, "main/schemas/all.html", data)


def schemas_new(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form_schema_new = SchemasNewForm(request.POST)
        if form_schema_new.is_valid():
            schema = form_schema_new.save(commit=False)

            schema.user = request.user
            schema.save()
            messages.add_message(request, messages.SUCCESS, f"Your schema '{schema.name}' has been successfully "
                                                            "created.")
            return redirect("schemas")
    else:
        form_schema_new = SchemasNewForm()

    data = {
        "form_new": form_schema_new
    }

    return render(request, "main/schemas/new.html", data)


def schemas_delete(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    schema_to_delete = Schemas.objects.get(id=id)
    if schema_to_delete.user == request.user:
        schema_to_delete.delete()
        '''messages.add_message(request, messages.SUCCESS, "Your schema has been successfully "
                                                        "deleted.")'''

    return redirect("schemas")


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


def logout(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout_user(request)
    return redirect("home")
