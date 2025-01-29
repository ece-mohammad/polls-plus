#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def custom_logout(request: HttpRequest) -> HttpResponseRedirect:
    next_page: str = request.GET.get("next", "/")
    logout(request)
    return redirect(next_page)

