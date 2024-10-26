#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Views for polls application
"""
from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
    HttpResponseBadRequest, HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView
)

from polls.models import Question, Choice


def owner_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Hello, world. {user_id} is the polls index.".format(
            user_id="c3d67032"
        )
    )


class PollsHomeView(ListView):
    model = Question
    template_name = "polls/home.html"
    context_object_name = "polls"
    queryset = Question.polls.most_recent(count=settings.RECENT_POLLS_SIZE)


class PollsListView(ListView):
    models = Question
    template_name = "polls/poll_list.html"
    context_object_name = "polls"
    queryset = Question.polls.published()


class PollDetailView(DetailView):
    model = Question
    template_name = "polls/poll_details.html"
    slug_url_kwarg = "poll_id"
    slug_field = "id"
    context_object_name = "poll"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.check_voted():
            context_data["voted"] = True
        return context_data

    def check_voted(self):
        voted_polls = self.request.session.get("votes", None)
        if voted_polls is not None:
            return self.object.id in voted_polls
        return False


class PollResultsView(DetailView):
    model = Question
    template_name = "polls/poll_results.html"
    slug_url_kwarg = "poll_id"
    slug_field = "id"
    context_object_name = "poll"


class PollVoteView(UpdateView):
    model = Question

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.method.lower() != "post":
            return HttpResponseNotAllowed(["POST"])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        poll_id = kwargs["poll_id"]
        redirect_url = "polls:poll_details"
        url_kwargs = {"poll_id": poll_id}

        question = get_object_or_404(Question, id=poll_id)
        if not question.is_published() or question.is_closed_for_voting():
            return HttpResponseNotAllowed("Poll is closed.")

        try:
            choice_id: int = int(request.POST["choice"])
        except KeyError:
            return HttpResponseBadRequest("Choice ID was not provided.")

        try:
            choice: Choice = question.choices.get(id=choice_id)
        except Choice.DoesNotExist:
            return HttpResponseNotFound("Choice was not found.")

        choice.votes += 1
        choice.save()
        self.mark_question_as_voted(poll_id)
        return HttpResponseRedirect(
            reverse_lazy(redirect_url, kwargs=url_kwargs)
        )

    def mark_question_as_voted(self, poll_id: int):
        voted_questions = self.request.session.get("votes", None)
        if voted_questions is None:
            voted_questions = [poll_id]
        elif poll_id not in voted_questions:
            voted_questions.append(poll_id)
        self.request.session["votes"] = voted_questions

"""

class PollCreateView(CreateView):
    model = Question
    fields = ("question_text",)
    template_name = "polls/poll_add.html"

    # success_url = reverse_lazy("polls:index")

    # def get_success_url(self):
    #     return reverse_lazy(
    #         "polls:question_details",
    #         kwargs={
    #             "question_id": self.object.id
    #         }
    #     )
    #
    # def post(self, request: HttpRequest, *args, **kwargs):
    #     request.POST["user"] = self.request.user
    #     request.POST["pub_date"] = datetime.now()
    #     return super(request, *args, **kwargs)


class PollUpdateView(UpdateView):
    model = Question
    fields = ["question_text"]
    template_name = "polls/poll_edit.html"
    slug_field = "id"
    slug_url_kwarg = "poll_id"

    def get_success_url(self):
        return reverse_lazy(
            "polls:polls_details",
            kwargs={
                "poll_id": self.object.id
            }
        )


class PollDeleteView(DeleteView):
    model = Question
    template_name = "polls/poll_delete.html"
    success_url = reverse_lazy("polls:index")

"""
