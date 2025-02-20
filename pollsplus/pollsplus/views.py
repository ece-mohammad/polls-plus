#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def about_view(request):
    return HttpResponseRedirect(reverse_lazy("home:home"))


def contact_view(request):
    return HttpResponseRedirect(reverse_lazy("home:home"))
