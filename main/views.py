from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as login_user,
    logout as logout_user
)
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from pathlib import Path

from main.forms import SchemasNewForm, SchemasNewCategories, SchemasColumnFormset, DatasetForm
from main.models import Schemas, DataSets
from .tasks import generate_file_async


def home(response):
    if not response.user.is_authenticated:
        return redirect("login")

    return render(response, "main/home.html", {"nav_home": True})


def schemas(request):
    """Getting list of all user Schemas"""
    if not request.user.is_authenticated:
        return redirect("login")

    user_schemas = Schemas.objects.all().filter(user=request.user)

    data = {
        "schemas": user_schemas,
        "nav_schemas": True
    }

    return render(request, "main/schemas/all.html", data)


def schemas_new(request):
    """Creating new Schema"""
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form_schema_new = SchemasNewForm(request.POST)
        formset_schema_column = SchemasColumnFormset(request.POST)

        if form_schema_new.is_valid() and formset_schema_column.is_valid():
            # Getting new schema and saving it to user
            schema = form_schema_new.save(commit=False)
            schema.user = request.user
            schema.save()

            # Getting deleted rows from form to ignore them latter
            marked_for_delete = formset_schema_column.deleted_forms

            for form in formset_schema_column.forms:
                # Adding columns to schema without deleted
                if form not in marked_for_delete:
                    column = form.save(commit=False)
                    column.schema = schema
                    column.save()

            messages.add_message(request, messages.SUCCESS, f"Your schema '{schema.name}' has been successfully "
                                                            "created.")
            return redirect("schemas")

        elif len(formset_schema_column) == 1 and form_schema_new.is_valid():
            # Check if form have at least one column
            messages.add_message(request, messages.ERROR, f"Please add at least one column")

    else:
        form_schema_new = SchemasNewForm()
        formset_schema_column = SchemasColumnFormset()

    data = {
        "form_new": form_schema_new,
        "form_add_category": SchemasNewCategories(),
        "form_set": formset_schema_column,
        "nav_schemas": True
    }

    return render(request, "main/schemas/new.html", data)


def schemas_delete(request, id):
    """Deleting schema if it user property"""
    if not request.user.is_authenticated:
        return redirect("login")

    schema_to_delete = Schemas.objects.get(id=id)
    if schema_to_delete.user == request.user:
        schema_to_delete.delete()

    return redirect("schemas")


def dataset(request, id):
    """Showing user dataset from schema """
    if not request.user.is_authenticated:
        return redirect("login")

    schema = Schemas.objects.filter(id=id, user=request.user)

    if schema.exists():
        # Getting correct schema and list of datasets
        schema = Schemas.objects.get(id=id)
        datasets = DataSets.objects.filter(schema=schema)

        if request.method == "POST":
            # Getting value from form and start generating file according to schema
            dataset_form = DatasetForm(request.POST)
            if dataset_form.is_valid():
                # Adding schema to freshly created dataset
                dataset_form = dataset_form.save(commit=False)
                dataset_form.schema = schema
                dataset_form.save()

                # Getting user directory location
                user_dir = settings.MEDIA_ROOT / f"user_{request.user.id}"

                # Sending file generation to Celery | Redis
                generate_file_async.apply_async((dataset_form.id, str(user_dir)))

                messages.add_message(request, messages.SUCCESS, "All clear, now please wait till Python generate file "
                                                                "and AJAX update status")
                return redirect("dataset", id)
        else:
            dataset_form = DatasetForm()

        data = {
            "name": schema.name,
            "datasets": datasets,
            "form": dataset_form,
            "schema_id": schema.id,
            "nav_schemas": True
        }

        return render(request, "main/datasets.html", data)
    else:
        # If schema does not belong to current user
        messages.add_message(request, messages.ERROR, "It is seems, that it is not your dataset.")
        return redirect("home")


def dataset_status(request, id):
    """Special function for AJAX, cheking for dataset file creation status"""
    dataset_data = DataSets.objects.get(id=id)
    result = {
        "dataset_status": dataset_data.ready
    }
    return JsonResponse(result, status=200)


def download(request, id_schema, id_dataset):
    """Getting requested dataset from schema to download"""
    if not request.user.is_authenticated:
        return redirect("login")

    dataset_download = DataSets.objects.filter(id=id_dataset)

    if dataset_download.exists():
        dataset_download = DataSets.objects.get(id=id_dataset)
        # Check for user
        if dataset_download.schema.user != request.user:
            messages.add_message(request, messages.ERROR, "It is seems, that it is not your dataset.")
        # Check for ready file
        elif not dataset_download.ready:
            messages.add_message(request, messages.ERROR, "Your data set is not ready yet, but still you guessed its "
                                                          "id :).")
        # Updating request with file
        else:
            filename = dataset_download.file.path
            with open(filename, 'rb') as fh:
                request = HttpResponse(fh.read(), content_type="text/csv")
                request['Content-Disposition'] = f'inline; filename={Path(filename).name}'
                return request
    else:
        messages.add_message(request, messages.ERROR, "It is seems, that this dataset does not exist :(")

    return redirect("dataset", id_schema)


def login(request):
    """Simple login"""
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
    """Simple logout"""
    if not request.user.is_authenticated:
        return redirect("login")
    logout_user(request)
    return redirect("home")
