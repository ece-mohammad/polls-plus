#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import (
    BaseValidator,
    MinLengthValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history import register
from simple_history.models import HistoricalRecords

from utils.helpers import human_readable_size

register(User)


class AdTitleValidator(BaseValidator):

    def __init__(self, limit_value, message: str = None):
        super().__init__(
            limit_value,
            message=_(f"Title must be at least {limit_value} characters long.")
        )

    def compare(self, a, b):
        return len(a) < b

    def clean(self, title: str):
        return title.strip()


class PictureSizeValidator(BaseValidator):

    def __init__(self, max_size, message: str = None):
        super().__init__(
            max_size,
            message=_(
                f"Image size must be less than {human_readable_size(max_size)}"
            )
        )

    def compare(self, a, b):
        if a.size > b:
            return True
        return False



class AdComment(models.Model):
    class Meta:
        ordering = ["-created_at"]

    ad = models.ForeignKey(
        "Ad",
        on_delete=models.CASCADE,
        verbose_name="Ad",
        help_text=_("Ad that this comment belongs to"),
        related_name="comments",
        related_query_name="comment",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Created by",
        help_text=_("User that created the comment"),
        null=True,
    )
    text = models.TextField(
        verbose_name="Comment",
        help_text=_("Comment for your advertisement"),
        validators=[
            MinLengthValidator(
                2,
                _("Comment must be at least 2 characters long")
            )
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
        help_text=_("When the comment was created")
    )

    def __str__(self):
        return f"Comment for {self.ad.title}: {self.text}"


class AdFavorite(models.Model):
    class Meta:
        unique_together = ("ad", "user")

    ad = models.ForeignKey(
        "Ad",
        on_delete=models.CASCADE,
        verbose_name="Ad",
        help_text=_("Ad that this favorite belongs to"),
        related_name="+",
        related_query_name="+",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Created by",
        help_text=_("User that created the favorite"),
        related_name="+",
    )


class Ad(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Created by",
        help_text=_("User that created the advertisement")
    )
    title = models.CharField(
        max_length=200,
        validators=[
            AdTitleValidator(2),
        ],
        blank=False,
        null=False,
        verbose_name="Title",
        help_text=_("Title for your advertisement")
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=False,
        default=Decimal(0.0),
        verbose_name="Price",
        help_text=_("Price for your advertisement")
    )
    text = models.TextField(
        null=True,
        default="",
        verbose_name="Description",
        help_text=_("Description for your advertisement")
    )
    picture = models.ImageField(
        verbose_name="Picture",
        help_text="Picture for your advertisement",
        upload_to="ads",
        null=True,
        blank=True,
        editable=True,
        validators=[
            PictureSizeValidator(
                settings.AD_PICTURE_MAX_SIZE,
                _(
                    f"Picture must be less than {human_readable_size(settings.AD_PICTURE_MAX_SIZE)}"
                )
            )
        ]
    )
    favored_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="AdFavorite",
        through_fields=("ad", "user"),
        blank=True,
        verbose_name="Favored by",
        help_text=_("Users that favorited the advertisement"),
        related_name="favorite_ads",
        related_query_name="favorite_ad",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
        help_text=_("When the advertisement was created")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
        help_text=_("Last time the advertisement was updated")
    )
    history = HistoricalRecords()

    def delete(self, *args, **kwargs):
        if self.picture:
            self.picture.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
