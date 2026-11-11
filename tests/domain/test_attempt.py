"""Responsibility: an Attempt knows whether the answer was right."""

import random

from math_tug.domain.attempt import Attempt
from math_tug.domain.problem import make_problem


def test_attempt_knows_if_it_was_right():
    problem = make_problem(random.Random(5))
    wrong = next(o for o in problem.options if o != problem.answer)
    assert Attempt(problem, problem.answer).correct is True
    assert Attempt(problem, wrong).correct is False
