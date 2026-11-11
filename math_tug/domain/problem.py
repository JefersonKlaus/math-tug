"""Random multiple-choice math problems."""

import random
from dataclasses import dataclass

from ..config import ADD_RANGE, OPTION_COUNT, SUB_RANGE, TABLE_CHOICES, TIMES_RANGE

OPERATIONS = ("+", "-", "×", "÷")
# Offsets used to build wrong options that look plausible next to the answer.
DISTRACTOR_OFFSETS = (-10, -2, -1, 1, 2, 10)


@dataclass(frozen=True)
class Problem:
    expression: str
    answer: int
    options: tuple[int, ...]


def _operands(rng: random.Random, operation: str, tables: tuple[int, ...]) -> tuple[int, int, int]:
    if operation == "+":
        a, b = rng.randint(*ADD_RANGE), rng.randint(*ADD_RANGE)
        return a, b, a + b
    if operation == "-":
        a = rng.randint(*SUB_RANGE)
        b = rng.randint(SUB_RANGE[0], a)
        return a, b, a - b
    table, times = rng.choice(tables), rng.randint(*TIMES_RANGE)
    if operation == "×":
        return table, times, table * times
    return table * times, table, times


def _options(rng: random.Random, answer: int) -> tuple[int, ...]:
    candidates = [answer + offset for offset in DISTRACTOR_OFFSETS if answer + offset >= 0]
    options = [answer, *rng.sample(candidates, OPTION_COUNT - 1)]
    rng.shuffle(options)
    return tuple(options)


def make_problem(rng: random.Random, operations: tuple[str, ...] = OPERATIONS, tables: tuple[int, ...] = TABLE_CHOICES) -> Problem:
    operation = rng.choice(operations)
    a, b, answer = _operands(rng, operation, tables)
    return Problem(f"{a} {operation} {b}", answer, _options(rng, answer))
