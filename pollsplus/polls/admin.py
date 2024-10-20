#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Admin site for polls application
"""

from django.contrib import admin

from polls.models import Question, Choice

admin.site.site_title = "Polls+"
admin.site.site_header = "Polls+ Administration"
admin.site.index_title = "Polls+ Administration"

# TODO:: add user

# Register your models here.
class QuestionModelAdmin(admin.ModelAdmin):
    # list_display_links = ["user", "question_text"]
    list_display_links = ["question_text"]
    # list_display = ["id", "user", "question_text", "pub_date"]
    list_display = ["id", "question_text", "pub_date"]
    # list_filter = ["user", "pub_date"]
    list_filter = ["pub_date"]
    sortable_by = ["id", "pub_date"]


class ChoiceModelAdmin(admin.ModelAdmin):
    list_display_links = ["choice_text"]
    list_display = ["id", "choice_text", "question", "votes"]
    sortable_by = ["id", "votes"]


admin.site.register(Question, QuestionModelAdmin)
admin.site.register(Choice, ChoiceModelAdmin)
