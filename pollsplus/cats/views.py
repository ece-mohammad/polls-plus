from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView
)

from cats.forms import BreedForm, CatForm
from cats.models import Breed, Cat


# Create your views here.

class BreedListView(LoginRequiredMixin, ListView):
    model = Breed


class BreedDetailView(LoginRequiredMixin, DetailView):
    model = Breed


class BreedCreateView(LoginRequiredMixin, CreateView):
    model = Breed
    form_class = BreedForm
    template_name = "cats/breed_create.html"
    success_url = reverse_lazy("cats:cats_list")


class BreedUpdateView(LoginRequiredMixin, UpdateView):
    model = Breed
    form_class = BreedForm
    template_name = "cats/breed_update.html"
    success_url = reverse_lazy("cats:cats_list")


class BreedDeleteView(LoginRequiredMixin, DeleteView):
    model = Breed
    success_url = reverse_lazy("cats:cats_list")


class CatListView(LoginRequiredMixin, ListView):
    model = Cat
    extra_context = {"breed_count": Breed.objects.count()}


class CatDetailView(LoginRequiredMixin, DetailView):
    model = Cat


class CatCreateView(LoginRequiredMixin, CreateView):
    model = Cat
    form_class = CatForm
    template_name = "cats/cat_create.html"
    success_url = reverse_lazy("cats:cats_list")


class CatUpdateView(LoginRequiredMixin, UpdateView):
    model = Cat
    form_class = CatForm
    template_name = "cats/cat_update.html"
    success_url = reverse_lazy("cats:cats_list")


class CatDeleteView(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = reverse_lazy("cats:cats_list")
