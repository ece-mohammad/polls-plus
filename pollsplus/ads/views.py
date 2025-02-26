#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import (
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import View

from ads.forms import AdCommentForm, AdForm
from ads.models import Ad, AdComment, AdFavorite
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

    def get_queryset(self):
        qs = super().get_queryset()
        search_query = self.request.GET.get("q", None)
        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(text__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).select_related()
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            context["fav_list"] = Ad.objects.filter(
                favored_by=user
            ).values_list("id", flat=True)
        return context



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


@method_decorator(csrf_exempt, name="dispatch")
class AdFavoriteToggleView(LoginRequiredMixin, UserListView):
    model = AdFavorite

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        rsp = {"favorites": []}
        for fav in context["object_list"]:
            rsp["favorites"].append(fav.ad.id)
        return JsonResponse(rsp)

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        post_data: dict = json.loads(request.body)

        ad_id: int = post_data["ad_id"]
        add_fav: bool = post_data["fav"]

        ad: Ad = get_object_or_404(Ad, pk=ad_id)
        user: User = self.request.user
        if add_fav:
            ad.favored_by.add(user)
            ad.save()
        else:
            fav: AdFavorite = get_object_or_404(AdFavorite, ad=ad, user=user)
            fav.delete()
        return JsonResponse({"status": 200})


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(require_http_methods(["POST"]), name="dispatch")
class AdFavoriteAddView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, *args, **kwargs):
        ad: Ad = get_object_or_404(Ad, pk=kwargs["pk"])
        ad.favored_by.add(request.user)
        ad.save()
        return JsonResponse({"status": 200})


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(require_http_methods(["POST"]), name="dispatch")
class AdFavoriteRemoveView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        fav: AdFavorite = get_object_or_404(
            AdFavorite,
            user=request.user,
            ad__pk=kwargs["pk"]
        )
        fav.delete()
        return JsonResponse({"status": 200})


class AdFavoriteListView(LoginRequiredMixin, UserListView):
    model = AdFavorite

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(user=self.request.user)
        return qs

    def render_to_response(self, context, **response_kwargs):
        rsp = {"favorites": []}
        for fav in context["object_list"]:
            rsp["favorites"].append(fav.ad.id)
        return JsonResponse(rsp)
