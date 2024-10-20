#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Models for polls application
"""
import datetime
from datetime import timedelta

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

"""
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType

# TODO: add permissions & group
class PollsUser(User):
    class Meta:
        permissions = []

# TODO: add permissions & group
class PollsModerator(User):
    class Meta:
        permissions = []

"""


class DefaultPollsManager(models.Manager):
    ...


class SortedPollsManager(DefaultPollsManager):
    ORDER_KEY = "-pub_date"


class PollsManager(SortedPollsManager):
    def by_pub_date(self):
        """Return all polls sorted by publish date"""
        return self.get_queryset().order_by(self.ORDER_KEY)

    def unpublished(self):
        """Get polls that are not published.

        A poll is unpublished if its pub_date has not come yet, or it has less
        than 2 choices.
        """
        return self.annotate(
            choice_count=models.Count("choice")
        ).filter(
            pub_date__gt=timezone.now(),
            choice_count__lt=2
        ).order_by(self.ORDER_KEY).prefetch_related("choices")

    def published(self):
        """Get all the published polls.

        A poll is published when its pub_date has passed. And has at least 2
        choices.
        """
        return self.annotate(
            choice_count=models.Count("choice")
        ).filter(
            pub_date__lte=timezone.now(),
            choice_count__gt=1
        ).order_by(self.ORDER_KEY).prefetch_related("choices")

    def closed_for_vote(self):
        """Return all polls that are closed for voting.

        A poll is closed for voting if its exp_date has passed.
        """
        return self.filter(
            exp_date__lte=timezone.now()
        ).order_by(self.ORDER_KEY)

    def open_for_vote(self):
        """Get all polls that are open for voting.

        A poll is open for voting if it's published and not expired.
        """
        return self.annotat(
            choice_count=models.Count("choice")
        ).filter(
            pub_date__lte=timezone.now(),
            exp_date__gt=timezone.now(),
            choice_count__gt=1
        ).order_by(self.ORDER_KEY).prefetch_related("choices")

    def closed_no_votes(self):
        """Return all closed poll that have zero votes."""
        return self.annotate(
            vote_count=models.Sum("choice__votes")
        ).filter(
            exp_date__lte=timezone.now(),
            vote_count=0
        ).order_by(self.ORDER_KEY).prefetch_related("choices")

    def published_no_votes(self):
        """Return polls that published and have no votes."""
        return self.annotate(
            choice_count=models.Count("choice"),
            vote_count=models.Sum("choice__votes")
        ).filter(
            pub_date__lte=timezone.now(),
            exp_date__gt=timezone.now(),
            choice_count__gt=1,
            vote_count=0
        ).order_by(self.ORDER_KEY).prefetch_related("choices")

    def most_voted(self, count: int | None = None) -> models.QuerySet:
        """Return N most voted questions of all time."""
        qs = self.annotate(
            vote_count=models.Sum("choice__votes")
        ).order_by(
            "-vote_count"
        ).prefetch_related("choices")

        if count is None:
            return qs
        return qs[:count]

    def most_recent(self, count: int | None = None) -> QuerySet:
        """
        Get most recent N poll questions ordered by ORDER_KEY.

        :param count: number of questions to retrieve, default is 5.
        :type count: int
        :return: N most recent questions, ordered by ORDER_KEY.
        :rtype: QuerySet
        """
        qs = self.published()
        if count is None:
            return qs
        return qs[:count]

    def expires_within(
        self,
        start: datetime.datetime = timezone.now(),
        end: datetime.datetime = timezone.now() + timedelta(days=1)
    ) -> QuerySet:
        """Get published polls that are about to expire within a period of time.

        :param start: start of the expiry period
        :type start: datetime.datetime
        :param end: the end of the expiry period
        :type end: datetime.datetime
        :return: list of questions that are about to expire
        :rtype: QuerySet
        """
        return self.filter(
            pub_date__lte=timezone.now(),
            exp_date__gte=start,
            exp_date__lte=end
        )

    def about_to_expire(self, count: int | None = None):
        """Get the first N polls that are about to expire."""
        qs = self.expires_within(
            start=timezone.now(),
            end=timezone.now() + timedelta(days=1),
        )
        if count is None:
            return qs
        return qs[:count]

    def oldest(self):
        """Get the oldest question."""
        return self.order_by(self.ORDER_KEY).last()

    def newest(self):
        """Get the most recent question."""
        return self.order_by(self.ORDER_KEY).first()


# TODO:: add user

class Question(models.Model):
    class Meta:
        ordering = ["-pub_date"]
        indexes = [
            models.Index(fields=("pub_date",)),
            models.Index(fields=("exp_date",)),
            models.Index(fields=("pub_date", "exp_date",)),
        ]

    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name="questions",
    #     related_query_name="question"
    # )
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date the poll is available for voting.")
    exp_date = models.DateTimeField("Date the poll is closed for voting.")

    # managers
    objects = DefaultPollsManager()
    polls = PollsManager()

    def is_published(self):
        """Check if current question is published"""
        return self.pub_date <= timezone.now() and self.choices.count() >= 2

    def is_unpublished(self):
        """Check if current question is unpublished"""
        return not self.is_published()

    def is_open_for_voting(self):
        """Check if current question is open for voting"""
        return self.is_published() and (timezone.now() < self.exp_date)

    def is_closed_for_voting(self):
        """Check if current question is closed for voting"""
        return not self.is_open_for_voting()

    def is_recent(self) -> bool:
        """
        Check if the question was created recently.

        :return: True if the question was published within the last day.
        :rtype: bool
        """
        now = timezone.now()
        day_ago = now - timedelta(days=1)
        return day_ago <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="choices",
        related_query_name="choice"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
