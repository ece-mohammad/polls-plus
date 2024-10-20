#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Provide helper functions for polls tests
"""
from datetime import timedelta, datetime
from itertools import zip_longest
from typing import List, Tuple

from polls.models import Question


def create_question(
    question_text: str,
    choices: List[str] | Tuple[str] | None = None,
    votes: List[int] | Tuple[int] | None = None,
    pub_date: datetime = datetime.now(),
    exp_date: datetime | None = None) -> Question:
    """
    Create a new question with publish date equal to current time,
    with an optional time offset.

    :param question_text: question's text
    :type question_text: str
    :param choices: choices' texts to be added to the question
    :type choices: Tuple[str]
    :param votes: votes for each choice, each vote is mapped to its choice by
    index. Extra choices are assumed to have 0 votes.
    :type votes: Tuple[int]
    :param pub_date: question's publish date, default is now
    :type pub_date: datetime.datetime
    :param exp_date: question expiry date, default is now + 30 days
    :type exp_date: datetime.datetime
    :return: A new question instance
    :rtype: Question
    """
    if exp_date is None:
        exp_date = pub_date + timedelta(days=30)

    question: Question = Question.polls.create(
        question_text=question_text,
        pub_date=pub_date,
        exp_date=exp_date
    )

    if choices is None:
        return question

    if votes is None:
        votes = list()

    for choice, vote in zip_longest(choices, votes, fillvalue=0):
        question.choices.create(
            choice_text=choice,
            votes=vote
        )

    return question
