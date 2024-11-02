from django.urls import path
from cats.views import (
    BreedCreateView, BreedDetailView, BreedListView, BreedUpdateView, BreedDeleteView,
    CatCreateView, CatDetailView, CatListView, CatUpdateView, CatDeleteView
)

app_name = "cats"

urlpatterns = [
    path("", CatListView.as_view(), name="cats_list"),
    path("main/<int:pk>/", CatDetailView.as_view(), name="cat_details"),
    path("main/create/", CatCreateView.as_view(), name="cat_create"),
    path("main/<int:pk>/update/", CatUpdateView.as_view(), name="cat_update"),
    path("main/<int:pk>/delete/", CatDeleteView.as_view(), name="cat_delete"),

    path("lookup/", BreedListView.as_view(), name="breeds_list"),
    path("lookup/<int:pk>/", BreedDetailView.as_view(), name="breed_details"),
    path("lookup/create/", BreedCreateView.as_view(), name="breed_create"),
    path("lookup/<int:pk>/update/", BreedUpdateView.as_view(), name="breed_update"),
    path("lookup/<int:pk>/delete/", BreedDeleteView.as_view(), name="breed_delete"),
]