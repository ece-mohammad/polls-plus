from django.urls import path

from autos.views import (
    AutoListView, AutoDetailView, AutoCreateView, AutoUpdateView, AutoDeleteView,
    MakeListView, MakeDetailView, MakeCreateView, MakeUpdateView,
    MakeDeleteView,
)

app_name = "autos"

urlpatterns = [
    path("", AutoListView.as_view(), name="auto_list"),
    path("main/<int:pk>/", AutoDetailView.as_view(), name="auto_details"),
    path("main/create/", AutoCreateView.as_view(), name="auto_create"),
    path("main/<int:pk>/update/", AutoUpdateView.as_view(), name="auto_update"),
    path("main/<int:pk>/delete/", AutoDeleteView.as_view(), name="auto_delete"),

    path("lookup/", MakeListView.as_view(), name="make_list"),
    path("lookup/<int:pk>/", MakeDetailView.as_view(), name="make_details"),
    path("lookup/create/", MakeCreateView.as_view(), name="make_create"),
    path("lookup/<int:pk>/update/", MakeUpdateView.as_view(), name="make_update"),
    path("lookup/<int:pk>/delete/", MakeDeleteView.as_view(), name="make_delete"),
]
