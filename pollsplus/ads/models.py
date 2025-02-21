#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import (
    BaseValidator,
    MinLengthValidator,
    MaxLengthValidator
)
from django.db import models
from simple_history import register
from simple_history.models import HistoricalRecords

from utils.helpers import human_readable_size

register(User)


class AdTitleValidator(BaseValidator):

    def __init__(self, limit_value, message: str = None):
        super().__init__(
            limit_value,
            message=f"Title must be at least {limit_value} characters long."
        )

    def compare(self, a, b):
        return len(a) < b

    def clean(self, title: str):
        return title.strip()


class AdComment(models.Model):
    class Meta:
        ordering = ["-created_at"]

    ad = models.ForeignKey(
        "Ad",
        on_delete=models.CASCADE,
        verbose_name="Ad",
        help_text="Ad that this comment belongs to",
        related_name="comments",
        related_query_name="comment",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Created by",
        help_text="User that created the comment",
        null=True,
    )
    text = models.TextField(
        verbose_name="Comment",
        help_text="Comment for your advertisement",
        validators=[
            MinLengthValidator(2, "Comment must be at least 2 characters long")
        ]
    )
    image = models.ImageField(
        verbose_name="Image",
        help_text="Image for your advertisement",
        upload_to="ads",
        null=True,
        blank=True,
        validators=[
            MaxLengthValidator(
                settings.AD_IMAGE_MAX_SIZE,
                f"Image must be less than {human_readable_size(settings.AD_IMAGE_MAX_SIZE)} MB"
            )
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
        help_text="When the comment was created"
    )

    def __str__(self):
        return f"Comment for {self.ad.title}: {self.text}"

# Create your models here.
class Ad(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Created by",
        help_text="User that created the advertisement"
    )
    title = models.CharField(
        max_length=200,
        validators=[
            AdTitleValidator(2),
        ],
        blank=False,
        null=False,
        verbose_name="Title",
        help_text="Title for your advertisement"
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=False,
        default=Decimal(0.0),
        verbose_name="Price",
        help_text="Price for your advertisement"
    )
    text = models.TextField(
        null=True,
        default="",
        verbose_name="Description",
        help_text="Description for your advertisement"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
        help_text="When the advertisement was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
        help_text="Last time the advertisement was updated"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.title
