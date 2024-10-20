#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
unit tests for polls models (Question, Choice and PollsManager)
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from polls.models import Question
from polls.tests.utils import create_question


class QuestionModelIsRecentTest(TestCase):
    def test_with_future_question_expect_false(self):
        """
        Test that Question.is_recent() returns False when the
        question's publish date is in the future
        """
        future_question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(future_question.is_recent())

    def test_with_old_question_expect_false(self):
        old_question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=-1, minutes=-1)
        )
        self.assertFalse(old_question.is_recent())

    def test_with_recent_question_expect_true(self):
        recent_question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(
                hours=-23, minutes=-59, seconds=-59
            )
        )
        self.assertTrue(recent_question.is_recent())


class QuestionModelIsPublishedTest(TestCase):
    def test_with_old_question_and_no_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=-1)
        )
        self.assertFalse(question.is_published())

    def test_with_old_question_and_choices_expect_true(self):
        question: Question = create_question(
            "foo?",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=-1)
        )
        self.assertTrue(question.is_published())

    def test_with_future_question_and_no_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(question.is_published())

    def test_with_future_question_and_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(question.is_published())


class QuestionModelIsUnPublishedTest(TestCase):
    def test_with_old_question_and_no_choices_expect_true(self):
        question: Question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=-1)
        )
        self.assertTrue(question.is_unpublished())

    def test_with_old_question_and_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=-1)
        )
        self.assertFalse(question.is_unpublished())

    def test_with_future_question_and_no_choices_expect_true(self):
        question: Question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=1)
        )
        self.assertTrue(question.is_unpublished())

    def test_with_future_question_and_choices_expect_true(self):
        question: Question = create_question(
            "foo?",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=1)
        )
        self.assertTrue(question.is_unpublished())


class QuestionModelIsOpenForVotingTest(TestCase):
    def test_future_question_no_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(question.is_open_for_voting())

    def test_with_future_question_and_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(question.is_open_for_voting())

    def test_with_old_question_no_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=-1)
        )
        self.assertFalse(question.is_open_for_voting())

    def test_with_old_question_and_no_choices_expect_false(self):
        question: Question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=-1)
        )
        self.assertFalse(question.is_open_for_voting())

    def test_with_old_question_and_choices_expect_true(self):
        question: Question = create_question(
            "foo?",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=-1)
        )
        self.assertTrue(question.is_open_for_voting())

    def test_with_expired_question_and_choices_false(self):
        question: Question = create_question(
            "foo?",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1)
        )
        self.assertFalse(question.is_open_for_voting())
