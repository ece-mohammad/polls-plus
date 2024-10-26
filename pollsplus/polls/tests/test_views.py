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
            ),
            choices=["bar", "ham", "spam"]
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
        create_question(
            "foo", pub_date=timezone.now() + timedelta(days=1),
            choices=["bar", "ham", "spam"]
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context["polls"], [])

    def test_past_and_future_questions_expect_past_question(self):
        past_question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=-1
            ),
            choices=["bar", "ham", "spam"]
        )
        future_question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=1
            ),
            choices=["bar", "ham", "spam"]
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
        for i in range(1, (settings.RECENT_POLLS_SIZE * 2) + 1):
            questions.append(
                create_question(
                    f"foo {i}",
                    choices=["bar", "ham", "spam"],
                    pub_date=timezone.now() + timedelta(days=-1, seconds=i)
                )
            )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)

        for i in range(
                settings.RECENT_POLLS_SIZE + 1,
                (settings.RECENT_POLLS_SIZE * 2) + 1
                ):
            self.assertContains(
                response,
                f"foo {i}"
            )
        self.assertQuerySetEqual(
            response.context["polls"],
            questions[::-1][:settings.RECENT_POLLS_SIZE]
        )

    def test_past_question_with_no_choices_expect_not_in_view(self):
        question = create_question(
            "foo",
            pub_date=timezone.now() + timedelta(days=-1)
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context["polls"], [])

    def test_past_question_with_one_choice_expect_not_in_view(self):
        question = create_question(
            "foo",
            pub_date=timezone.now() + timedelta(days=-1),
            choices=["bar"]
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context["polls"], [])

    def test_expired_question_expect_not_in_view(self):
        question = create_question(
            "foo",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1),
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_home")
        )
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context["polls"], [])


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
            ),
            choices=["bar", "ham", "spam"]
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
        create_question("foo", pub_date=timezone.now() + timedelta(days=1), choices=["bar", "ham", "spam"])
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
            ),
            choices=["bar", "ham", "spam"]
        )
        future_question = create_question(
            "foo", pub_date=timezone.now() + timedelta(
                days=1
            ),
            choices=["bar", "ham", "spam"]
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
                    pub_date=timezone.now() + timedelta(days=-1),
                    choices=["bar", "ham", "spam"]
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

    def test_expired_question_expect_in_view(self):
        question = create_question(
            "foo",
            choices=["bar", "ham", "spam"],
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1),
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_list")
        )
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context["polls"], [question])

    def test_question_with_no_choices_expect_not_in_view(self):
        question = create_question(
            "foo",
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1),
        )
        response: HttpResponse = self.client.get(
            reverse_lazy("polls:polls_list")
        )
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context["polls"], [])


class PollsDetailsViewTest(TestCase):
    def test_poll_expect_question_text_and_choices_text(self):
        choices: List[str] = ["bar", "ham", "spam"]
        question: Question = create_question(
            "foo?",
            choices=choices,
        )
        response: HttpResponse = self.client.get(
            reverse_lazy(
                "polls:poll_details",
                kwargs={
                    "poll_id": question.id
                }
            )
        )

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, question.question_text)
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
                "polls:poll_vote",
                kwargs={
                    "poll_id": question.id
                }
            ),
            data={"choice": 1},
            follow=True
        )
        choice.refresh_from_db()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(choice.votes, 1)

    def test_submitting_choice_expect_vote_again_button(self):
        choices: List[str] = ["bar", "ham", "spam"]
        question: Question = create_question(
            "foo",
            choices=choices
        )
        choice: Choice = question.choices.first()
        response: HttpResponse = self.client.post(
            reverse_lazy(
                "polls:poll_vote",
                kwargs={
                    "poll_id": question.id
                }
            ),
            data={"choice": 1},
            follow=True
        )
        choice.refresh_from_db()

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Vote again?")

    def test_expired_question_expect_voting_is_not_enabled(self):
        choices: List[str] = ["bar", "ham", "spam"]
        question: Question = create_question(
            "foo",
            choices=choices,
            pub_date=timezone.now() + timedelta(days=-2),
            exp_date=timezone.now() + timedelta(days=-1),
        )
        response: HttpResponse = self.client.get(
            reverse_lazy(
                "polls:poll_details",
                kwargs={
                    "poll_id": question.id
                }
            )
        )

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Poll closed")


class PollsVoteViewTest(TestCase):
    def test_vote_question_expect_votes_incremented_by_one(self):
        ...

    def test_vote_non_existent_question_expect_error_404(self):
        ...

    def test_vote_non_existent_choice_id_expect_error_404(self):
        ...

    def test_vote_future_question_expect_error_not_allowed(self):
        ...

    def test_vote_question_with_no_choices_expect_error_not_allowed(self):
        ...

    def test_vote_expired_question_expect_error_not_allowed(self):
        ...

    def test_vote_question_without_choice_id_expect_error_bad_request(self):
        ...

    def test_vote_choice_for_another_question_expect_error_404(self):
        ...


class PollsResultsViewTest(TestCase):
    ...
