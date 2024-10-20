#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
URLs for polls application
"""

from django.urls import path

from polls.views import (PollsHomeView, PollsListView,
    PollDetailView, PollVoteView, PollResultsView, owner_view)

app_name = "polls"

urlpatterns = [
    path("", PollsHomeView.as_view(), name="polls_home"),
    path("owner/", owner_view, name="owner"),
    path("all/", PollsListView.as_view(), name="polls_list"),
    path("<int:poll_id>/", PollDetailView.as_view(), name="poll_details"),
    path("<int:poll_id>/vote", PollVoteView.as_view(), name="poll_vote"),
    path("<int:poll_id>/results", PollResultsView.as_view(), name="poll_result"),
    # path("new/", PollCreateView.as_view(), name="polls_new"),
    # path("<int:poll_id>/edit", PollUpdateView.as_view(), name="polls_edit"),
    # path("<int:poll_id>/delete", QuestionCreateView.as_view(), name="polls_delete"),
]
