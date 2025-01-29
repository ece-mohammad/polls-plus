#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from ads.models import Ad


class OwnerMixin(LoginRequiredMixin):
    """
    A Mixin to limit the user access to only their ads
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class UserListView(ListView):
    ...


class UserDetailView(DetailView):
    ...


class LoggedInUserCreateView(LoginRequiredMixin, CreateView):
    ...


class OwnerUpdateView(OwnerMixin, UpdateView):
    ...


class OwnerDeleteView(OwnerMixin, DeleteView):
    ...


# Create your views here.
class HomePageView(UserListView):
    model = Ad


class AdDetailView(UserDetailView):
    model = Ad


class AdCreateView(LoggedInUserCreateView):
    model = Ad
    fields = ["title", "price", "text"]
    success_url = reverse_lazy("ads:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AdUpdateView(OwnerUpdateView):
    model = Ad
    template_name_suffix = "_update_form"
    fields = ["title", "price", "text"]
    success_url = reverse_lazy("ads:home")

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy("ads:home")
