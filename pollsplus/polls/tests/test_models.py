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


class PollsManagerQuerySetTest(TestCase):
    def test_all_with_different_pub_date_expect_all_questions_ordered_by_pub_date(
        self):
        questions = list()
        for i in range(1, 11):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham", "spam"],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i)
                )
            )
        self.assertQuerySetEqual(
            Question.polls.all(), questions[::-1], ordered=False
        )

    def test_all_same_pub_date_expect_ordered_by_id(self):
        questions = list()
        for i in range(1, 11):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham", "spam"],
                    pub_date=timezone.now() + timedelta(days=-1)
                )
            )
        self.assertQuerySetEqual(
            Question.polls.all(), questions[::-1], ordered=False
        )


class PollsManagerPublishedTest(TestCase):
    def test_question_with_choices_expect_published(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now()
        )
        qs = Question.polls.published()
        self.assertQuerySetEqual(qs, [question])

    def test_question_without_choices_expect_not_published(self):
        question = create_question(
            "foo?",
            pub_date=timezone.now()
        )
        qs = Question.polls.published()
        self.assertQuerySetEqual(qs, [])

    def test_question_with_one_choice_expect_not_published(self):
        question = create_question(
            "foo?",
            choices=["bar"],
            pub_date=timezone.now()
        )
        qs = Question.polls.published()
        self.assertQuerySetEqual(qs, [])

    def test_future_question_with_choices_expect_not_published(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=1)
        )
        qs = Question.polls.published()
        self.assertQuerySetEqual(qs, [])

    def test_future_question_without_choices_expect_not_published(self):
        question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=1)
        )
        qs = Question.polls.published()
        self.assertQuerySetEqual(qs, [])

    def test_future_question_with_one_choice_expect_not_published(self):
        question = create_question(
            "foo?",
            choices=["bar"],
            pub_date=timezone.now() + timedelta(days=1)
        )
        qs = Question.polls.published()
        self.assertQuerySetEqual(qs, [])

    def test_expired_question_with_choices_expect_published(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1)
        )
        qs = Question.polls.published()
        self.assertQuerySetEqual(qs, [question])


class PollsManagerPublishedOpenForVoteTest(TestCase):
    def test_future_question_with_choices_expect_not_open(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=1)
        )
        qs = Question.polls.published_open_for_vote()
        self.assertQuerySetEqual(qs, [])

    def test_future_question_without_choices_expect_not_open(self):
        question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=1)
        )
        qs = Question.polls.published_open_for_vote()
        self.assertQuerySetEqual(qs, [])

    def test_question_with_choices_expect_open(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now()
        )
        qs = Question.polls.published_open_for_vote()
        self.assertQuerySetEqual(qs, [question])

    def test_question_without_choices_expect_not_open(self):
        question = create_question(
            "foo?",
            pub_date=timezone.now()
        )
        qs = Question.polls.published_open_for_vote()
        self.assertQuerySetEqual(qs, [])

    def test_expired_question_with_choices_expect_not_open(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1)
        )
        qs = Question.polls.published_open_for_vote()
        self.assertQuerySetEqual(qs, [])

    def test_expired_question_without_choices_expect_not_open(self):
        question = create_question(
            "foo?",
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1)
        )
        qs = Question.polls.published_open_for_vote()
        self.assertQuerySetEqual(qs, [])


class PollsManagerMostVotedTest(TestCase):
    def test_questions_with_no_votes_expect_all_questions(self):
        questions = list()
        for i in range(1, 10):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham"],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i),
                )
            )
        qs = Question.polls.most_voted()
        self.assertQuerySetEqual(qs, questions[::-1])

    def test_questions_with_votes_expect_most_voted_questions(self):
        questions = list()
        for i in range(1, 10):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham"],
                    votes=[i],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i),
                )
            )
        qs = Question.polls.most_voted()
        self.assertQuerySetEqual(qs, questions[::-1])

    def test_questions_with_votes_expect_most_voted_questions_order_by_votes(
        self):
        questions = list()
        for i in range(1, 10):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham"],
                    votes=[10 - i],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i),
                )
            )
        qs = Question.polls.most_voted()
        self.assertQuerySetEqual(qs, questions)

    def test_n_count_expect_n_questions(self):
        questions = list()
        for i in range(1, 10):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham"],
                    votes=[10 - i],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i),
                )
            )
        qs = Question.polls.most_voted(count=5)
        self.assertQuerySetEqual(qs, questions[:5])

    def test_expired_questions_expect_in_result(self):
        questions = list()
        questions.append(
            create_question(
                f"foo",
                choices=["bar", "ham"],
                pub_date=timezone.now() + timedelta(days=-2),
                exp_date=timezone.now() + timedelta(days=-1),
                votes=[10],
            )
        )
        for i in range(1, 10):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham"],
                    votes=[10 - i],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i),
                )
            )
        qs = Question.polls.most_voted(5)
        self.assertQuerySetEqual(qs, questions[:5])


class PollsManagerMostRecentTest(TestCase):
    def test_questions_with_no_choices_expect_not_in_result(self):
        question = create_question(
            "foo?",
            choices=[],
            pub_date=timezone.now() + timedelta(days=-1)
        )
        qs = Question.polls.most_recent()
        self.assertQuerySetEqual(qs, [])

    def test_future_questions_expect_not_in_result(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=1)
        )
        qs = Question.polls.most_recent()
        self.assertQuerySetEqual(qs, [])

    def test_expired_questions_expect_not_in_result(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1)
        )
        qs = Question.polls.most_recent()
        self.assertQuerySetEqual(qs, [])

    def test_past_expired_future_questions_expect_past_in_result(self):
        future_question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=2),
        )
        past_question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-1),
        )
        expired_question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1)
        )
        qs = Question.polls.most_recent()
        self.assertQuerySetEqual(qs, [past_question])

    def test_count_n_expect_n_most_recent_questions(self):
        questions = list()
        for i in range(1, 10):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham"],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i),
                )
            )
        qs = Question.polls.most_recent(count=5)
        self.assertQuerySetEqual(qs, questions[::-1][:5])


class PollsManagerAboutToExpireTest(TestCase):
    def test_future_question_expect_not_about_to_expire(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=1),
            exp_date=timezone.now() + timedelta(days=2)
        )
        qs = Question.polls.about_to_expire()
        self.assertQuerySetEqual(qs, [])

    def test_expired_question_expect_not_about_to_expire(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1)
        )
        qs = Question.polls.about_to_expire()
        self.assertQuerySetEqual(qs, [])

    def test_open_question_with_more_than_24hrs_expect_not_about_to_expire(
        self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-1),
            exp_date=timezone.now() + timedelta(days=2)
        )
        qs = Question.polls.about_to_expire()
        self.assertQuerySetEqual(qs, [])

    def test_open_question_with_less_than_24hrs_expect_about_to_expire(self):
        question = create_question(
            "foo?",
            choices=["bar", "ham"],
            pub_date=timezone.now() + timedelta(days=-1),
            exp_date=timezone.now() + timedelta(days=1)
        )
        qs = Question.polls.about_to_expire()
        self.assertQuerySetEqual(qs, [question])
