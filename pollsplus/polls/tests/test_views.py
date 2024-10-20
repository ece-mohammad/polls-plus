from datetime import timedelta
from typing import List

from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone

from polls.models import Question, Choice
from polls.tests.utils import create_question


class PollsHomeViewTest(TestCase):
    def test_no_questions_expect_empty_context(self):
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "No questions yet! Start by starting a new poll"
        )
        self.assertQuerySetEqual(response.context["polls"], [])

    def test_past_question_expect_in_view(self):
        question: Question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=-1
            )
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "foo"
        )
        self.assertQuerySetEqual(response.context["polls"], [question])

    def test_future_question_expect_not_in_view(self):
        create_question("foo", pub_date=timezone.now() + timedelta(days=1))
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "foo"
        )
        self.assertQuerySetEqual(response.context["polls"], [])

    def test_past_and_future_questions_expect_past_question(self):
        past_question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=-1
            )
        )
        future_question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=1
            )
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "foo"
        )
        self.assertQuerySetEqual(response.context["polls"], [past_question])

    def test_multiple_questions_expect_n_most_recent(self):
        questions = []
        for i in range(settings.RECENT_POLLS_SIZE * 2):
            questions.append(
                create_question(
                    f"foo {i + 1}",
                    choices=["bar", "ham", "spam"],
                    pub_date=timezone.now() + timedelta(days=-1)
                )
            )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)

        for i in range(settings.RECENT_POLLS_SIZE):
            self.assertContains(
                response,
                f"foo {i + settings.RECENT_POLLS_SIZE + 1}"
            )
        self.assertQuerySetEqual(
            response.context["polls"],
            questions[::-1][:settings.RECENT_POLLS_SIZE]
        )


class PollsListViewTest(TestCase):
    def test_no_questions_expect_empty_context(self):
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_list")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "No questions yet! Start by starting a new poll"
        )
        self.assertQuerySetEqual(response.context["polls"], [])

    def test_past_question_expect_in_view(self):
        question: Question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=-1
            )
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_list")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "foo"
        )
        self.assertQuerySetEqual(response.context["polls"], [question])

    def test_future_question_expect_not_in_view(self):
        create_question("foo", pub_date=timezone.now() + timedelta(days=1))
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_list")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "foo"
        )
        self.assertQuerySetEqual(response.context["polls"], [])

    def test_past_and_future_questions_expect_past_question(self):
        past_question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=-1
            )
        )
        future_question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=1
            )
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_list")
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(
            response,
            "foo"
        )
        self.assertQuerySetEqual(response.context["polls"], [past_question])

    def test_multiple_questions_expect_n_most_recent(self):
        questions = []
        for i in range(settings.RECENT_POLLS_SIZE * 2):
            questions.append(
                create_question(
                    f"foo {i + 1}",
                    pub_date=timezone.now() + timedelta(days=-1)
                )
            )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_list")
        )
        self.assertEquals(response.status_code, 200)

        for i in range(settings.RECENT_POLLS_SIZE):
            self.assertContains(
                response,
                f"foo {i + settings.RECENT_POLLS_SIZE + 1}"
            )
        self.assertQuerySetEqual(
            response.context["polls"],
            questions[::-1]
        )


class PollsDetailsViewTest(TestCase):
    def test_details_expect_choices_text(self):
        choices: List[str] = ["bar", "ham", "spam"]
        question: Question = create_question(
            "foo",
            choices=choices
        )
        response: HttpResponse = self.client.get(
            reverse_lazy(
                "polls:polls_details",
                kwargs={
                    "poll_id": question.id
                }
            )
        )

        self.assertEquals(response.status_code, 200)
        for ch in choices:
            self.assertContains(response, ch)

    def test_submitting_choice_expect_votes_increment_by_one(self):
        choices: List[str] = ["bar", "ham", "spam"]
        question: Question = create_question(
            "foo",
            choices=choices
        )
        choice: Choice = question.choices.first()
        response: HttpResponse = self.client.post(
            reverse_lazy(
                "polls:polls_vote",
                kwargs={
                    "poll_id": choice.id
                }
            ),
            data={"choice": 1},
            follow=True
        )
        choice.refresh_from_db()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(choice.votes, 1)


class PollsResultsViewTest(TestCase):
    ...


class PollsVoteViewTest(TestCase):
    def test_vote_question_expect_votes_incremented_by_one(self):
        ...

    def test_vote_non_existent_question_expect_error_404(self):
        ...

    def test_vote_non_existent_choice_expect_error_404(self):
        ...

    def test_vote_future_question_expect_error_not_allowed(self):
        ...
