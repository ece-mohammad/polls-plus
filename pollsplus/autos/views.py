from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from autos.forms import AutoForm, MakeForm
from autos.models import Make, Auto


# Create your views here.
class MakeRedirectView:
    success_url = reverse_lazy("autos:auto_list")


class MakeListView(LoginRequiredMixin, ListView):
    model = Make


class MakeDetailView(LoginRequiredMixin, DetailView):
    model = Make


class MakeCreateView(LoginRequiredMixin, MakeRedirectView, CreateView):
    model = Make
    form_class = MakeForm
    template_name = "autos/make_create.html"


class MakeUpdateView(LoginRequiredMixin, MakeRedirectView, UpdateView):
    model = Make
    form_class = MakeForm
    template_name = "autos/make_update.html"


class MakeDeleteView(LoginRequiredMixin, MakeRedirectView, DeleteView):
    model = Make


class AutoRedirectView:
    success_url = reverse_lazy("autos:auto_list")


class AutoListView(LoginRequiredMixin, ListView):
    model = Auto

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["make_count"] = Make.objects.count()
        return context


class AutoDetailView(LoginRequiredMixin, DetailView):
    model = Auto


class AutoCreateView(LoginRequiredMixin, AutoRedirectView, CreateView):
    model = Auto
    form_class = AutoForm
    template_name = "autos/auto_create.html"


class AutoUpdateView(LoginRequiredMixin, AutoRedirectView, UpdateView):
    model = Auto
    form_class = AutoForm
    template_name = "autos/auto_update.html"


class AutoDeleteView(LoginRequiredMixin, AutoRedirectView, DeleteView):
    model = Auto
