"""Responsibility: generated problems are correct, fair and multiple choice."""

import operator
import random
from collections import Counter

from math_tug.config import ADD_RANGE, OPTION_COUNT, SUB_RANGE, TABLE_CHOICES, TIMES_RANGE
from math_tug.domain.problem import OPERATIONS, Problem, make_problem

SOLVE = {"+": operator.add, "-": operator.sub, "×": operator.mul, "÷": operator.truediv}
SAMPLES = [make_problem(random.Random(seed)) for seed in range(400)]


def parse(problem: Problem):
    left, symbol, right = problem.expression.split()
    return int(left), symbol, int(right)


def test_answer_is_mathematically_correct():
    for problem in SAMPLES:
        left, symbol, right = parse(problem)
        assert SOLVE[symbol](left, right) == problem.answer, problem


def test_has_three_distinct_options_including_the_answer_once():
    for problem in SAMPLES:
        assert len(set(problem.options)) == OPTION_COUNT == len(problem.options), problem
        assert problem.options.count(problem.answer) == 1, problem


def test_numbers_are_whole_and_never_negative():
    for problem in SAMPLES:
        left, _, right = parse(problem)
        assert min(left, right, problem.answer, *problem.options) >= 0, problem
        assert all(isinstance(n, int) for n in (problem.answer, *problem.options)), problem


def test_every_operation_is_used():
    assert {parse(p)[1] for p in SAMPLES} == set(OPERATIONS)


def test_operands_stay_in_their_ranges():
    for problem in SAMPLES:
        left, symbol, right = parse(problem)
        if symbol == "+":
            assert ADD_RANGE[0] <= left <= ADD_RANGE[1] and ADD_RANGE[0] <= right <= ADD_RANGE[1]
        elif symbol == "-":
            assert SUB_RANGE[0] <= right <= left <= SUB_RANGE[1]
        elif symbol == "×":
            assert left in TABLE_CHOICES and TIMES_RANGE[0] <= right <= TIMES_RANGE[1]
        else:
            assert right in TABLE_CHOICES and TIMES_RANGE[0] <= problem.answer <= TIMES_RANGE[1]


def test_wrong_options_are_close_to_the_answer():
    for problem in SAMPLES:
        assert all(abs(option - problem.answer) in {0, 1, 2, 10} for option in problem.options), problem


def test_answer_position_is_shuffled():
    positions = Counter(p.options.index(p.answer) for p in SAMPLES)
    assert set(positions) == set(range(OPTION_COUNT))
    assert min(positions.values()) > len(SAMPLES) / OPTION_COUNT / 2


def test_zero_answer_still_gets_valid_options():
    class ZeroRng(random.Random):
        def choice(self, seq):
            return "-"

        def randint(self, a, b):
            return a  # 10 - 10 = 0

    problem = make_problem(ZeroRng(0))
    assert problem.answer == 0
    assert min(problem.options) == 0
    assert len(set(problem.options)) == OPTION_COUNT


def test_only_uses_the_given_operations():
    for seed in range(100):
        assert parse(make_problem(random.Random(seed), ("×", "÷")))[1] in ("×", "÷")


def test_multiplication_puts_the_chosen_table_first():
    for seed in range(100):
        left, _, right = parse(make_problem(random.Random(seed), ("×",), (7,)))
        assert left == 7 and TIMES_RANGE[0] <= right <= TIMES_RANGE[1]


def test_division_divides_by_the_chosen_table():
    for seed in range(100):
        problem = make_problem(random.Random(seed), ("÷",), (3, 9))
        left, _, right = parse(problem)
        assert right in (3, 9) and left == right * problem.answer
