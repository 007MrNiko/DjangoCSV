from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("schemas/", views.schemas, name="schemas"),
    path("schemas/delete/<int:id>/", views.schemas_delete, name="schemas_delete"),
    path("schemas/new/", views.schemas_new, name="schemas_new"),
    path("dataset/<int:id>/", views.dataset, name="dataset"),
    path("dataset/status/<int:id>/", views.dataset_status, name="dataset_status"),
    path("dataset/<int:id_schema>/download/<int:id_dataset>", views.download, name="download")
]
