#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest,
    HttpResponseRedirect
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import View

from ads.forms import AdCommentForm, AdForm
from ads.models import Ad, AdComment
from utils.views import (
    UserListView,
    UserDetailView,
    LoggedInUserCreateView,
    AuthorUpdateView,
    AuthorDeleteView
)


# Create your views here.
class HomePageView(UserListView):
    model = Ad


class AdDetailView(UserDetailView):
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = AdCommentForm()
        return context


class AdCreateView(LoggedInUserCreateView):
    model = Ad
    form_class = AdForm
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("ads:home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdateView(AuthorUpdateView):
    model = Ad
    form_class = AdForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("ads:home")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        self.old_picture = object.picture
        return object

    def form_valid(self, form):
        if self.old_picture and not form.cleaned_data["picture"]:
            self.old_picture.delete()

        elif self.old_picture and form.cleaned_data["picture"]:
            if self.old_picture != form.cleaned_data["picture"]:
                self.old_picture.delete()
                form.instance.picture = form.cleaned_data["picture"]

            else:
                form.instance.picture = self.old_picture
        form.instance.updated_at = timezone.now()
        return super(AdUpdateView, self).form_valid(form)


class AdDeleteView(AuthorDeleteView):
    model = Ad
    success_url = reverse_lazy("ads:home")


class AdCommentCreateView(LoginRequiredMixin, View):

    @method_decorator(require_http_methods(["POST"]))
    def dispatch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        self.ad = Ad.objects.get(pk=kwargs["pk"])
        comment_form = AdCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.ad = self.ad
            comment.save()
            return HttpResponseRedirect(
                reverse_lazy(
                    "ads:ad_details",
                    kwargs={"pk": self.ad.id}
                )
            )
        return redirect(
            reverse_lazy(
                "ads:ad_details",
                kwargs={"pk": self.ad.id}
            )
        )


class AdCommentUpdateView(AuthorUpdateView):
    model = AdComment
    fields = ("text",)
    template_name_suffix = "_update_form"

    def get_object(self, queryset=None):
        return AdComment.objects.get(pk=self.kwargs["comment_pk"])

    def get_success_url(self):
        return reverse_lazy(
            "ads:ad_details",
            kwargs={"pk": self.object.ad.id}
        )

    def form_valid(self, form):
        if super().form_valid(form):
            self.object.updated_at = timezone.now()
            self.object.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "ads:ad_details",
                kwargs={"pk": self.object.ad.id}
            )
        )


class AdCommentDeleteView(AuthorDeleteView):
    model = AdComment

    def get_object(self, queryset=None):
        return AdComment.objects.get(pk=self.kwargs["comment_pk"])

    def get_success_url(self):
        return reverse_lazy(
            "ads:ad_details",
            kwargs={"pk": self.object.ad.id}
        )
