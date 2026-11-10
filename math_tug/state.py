from dataclasses import dataclass
from enum import Enum

from .config import PROBLEMS


class Screen(Enum):
    LOBBY = "lobby"
    COUNTDOWN = "countdown"
    PLAYING = "playing"
    RESULT = "result"


@dataclass
class GameState:
    screen: Screen = Screen.LOBBY
    countdown: int = 3
    problem_index: int = 0
    player_score: int = 4
    opponent_score: int = 3

    @property
    def current_problem(self) -> tuple[str, str]:
        return PROBLEMS[self.problem_index]

    @property
    def is_last_problem(self) -> bool:
        return self.problem_index == len(PROBLEMS) - 1

    def reset(self):
        self.screen = Screen.LOBBY
        self.countdown = 3
        self.problem_index = 0
        self.player_score = 4
        self.opponent_score = 3
