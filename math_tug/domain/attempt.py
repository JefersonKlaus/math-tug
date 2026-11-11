"""A player's answer to a problem."""

from dataclasses import dataclass

from .problem import Problem


@dataclass(frozen=True)
class Attempt:
    problem: Problem
    choice: int

    @property
    def correct(self) -> bool:
        return self.choice == self.problem.answer
