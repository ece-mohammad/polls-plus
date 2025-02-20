#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["invalid_login"] = _(
            "Your username and password didn't match. Please try again. "
            "Note that both fields are case-sensitive."
        )
