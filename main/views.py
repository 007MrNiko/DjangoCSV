from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers
from django.contrib.auth import (
    authenticate,
    login as login_user,
    logout as logout_user
)
from django.contrib import messages

from main.models import Schemas, DataSets, user_directory_path
from main.forms import SchemasNewForm, SchemasNewCategories, SchemasColumnFormset, DatasetForm

from extensions import generate_file
from .tasks import generate_file_async


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
        formset_schema_column = SchemasColumnFormset(request.POST)

        if form_schema_new.is_valid() and formset_schema_column.is_valid():
            schema = form_schema_new.save(commit=False)
            schema.user = request.user
            schema.save()

            marked_for_delete = formset_schema_column.deleted_forms

            for form in formset_schema_column.forms:
                # so that `book` instance can be attached.
                if form not in marked_for_delete:
                    column = form.save(commit=False)
                    column.schema = schema
                    column.save()

            messages.add_message(request, messages.SUCCESS, f"Your schema '{schema.name}' has been successfully "
                                                            "created.")
            return redirect("schemas")

        elif len(formset_schema_column) == 1 and form_schema_new.is_valid():
            messages.add_message(request, messages.ERROR, f"Please add at least one column")

    else:
        form_schema_new = SchemasNewForm()
        formset_schema_column = SchemasColumnFormset()

    data = {
        "form_new": form_schema_new,
        "form_add_category": SchemasNewCategories(),
        "form_set": formset_schema_column
    }

    return render(request, "main/schemas/new.html", data)


def schemas_delete(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    schema_to_delete = Schemas.objects.get(id=id)
    if schema_to_delete.user == request.user:
        schema_to_delete.delete()

    return redirect("schemas")


def dataset(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    schema = Schemas.objects.filter(id=id, user=request.user)

    if schema.exists():
        schema = Schemas.objects.get(id=id)
        datasets = DataSets.objects.filter(schema=schema)

        if request.method == "POST":
            dataset_form = DatasetForm(request.POST)
            if dataset_form.is_valid():
                dataset_form = dataset_form.save(commit=False)
                dataset_form.schema = schema
                dataset_form.save()

                user_dir = settings.MEDIA_ROOT / f"user_{request.user.id}"

                #generate_file(dataset_form, user_dir)
                generate_file_async.apply_async((dataset_form.id, str(user_dir)))

                messages.add_message(request, messages.SUCCESS, "Your dataset has been successfully "
                                                                "created.")
                return redirect("dataset", id)
        else:
            dataset_form = DatasetForm()

        data = {
            "name": schema.name,
            "datasets": datasets,
            "form": dataset_form,
            "schema_id": schema.id
        }

        return render(request, "main/datasets.html", data)
    else:
        messages.add_message(request, messages.ERROR, "It is seems, that it is not your dataset.")
        return redirect("home")


def dataset_status(request, id):
    dataset_data = DataSets.objects.get(id=id)
    result = {
        "dataset_status": dataset_data.ready
    }
    return JsonResponse(result, status=200)


def download(request, id_schema, id_dataset):
    if not request.user.is_authenticated:
        return redirect("login")

    dataset_download = DataSets.objects.filter(id=id_dataset)

    if dataset_download.exists():
        dataset_download = DataSets.objects.get(id=id_dataset)
        if dataset_download.schema.user != request.user:
            messages.add_message(request, messages.ERROR, "It is seems, that it is not your dataset.")
        elif not dataset_download.ready:
            messages.add_message(request, messages.ERROR, "Your data set is not ready yet, but still you guessed its "
                                                          "id :).")
        else:
            filename = dataset_download.file.path
            request = FileResponse(open(filename, 'rb'), "text/csv")
            return request
    else:
        messages.add_message(request, messages.ERROR, "It is seems, that this dataset does not exist :(")

    return redirect("dataset", id_schema)


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
