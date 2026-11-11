"""Where the app is (which screen) and the state of the current game."""

from dataclasses import dataclass, field
from enum import Enum

from ..i18n import DEFAULT_LANGUAGE
from .attempt import Attempt
from .player import Player
from .problem import Problem
from .settings import Settings


class Screen(Enum):
    LOBBY = "lobby"
    COUNTDOWN = "countdown"
    PLAYING = "playing"
    RESULT = "result"
    SETTINGS = "settings"


def _per_player(value):
    return lambda: {player: value for player in Player}


@dataclass
class GameState:
    screen: Screen = Screen.LOBBY
    countdown: int = 3
    scores: dict[Player, int] = field(default_factory=_per_player(0))
    problems: dict[Player, Problem | None] = field(default_factory=_per_player(None))
    last_attempts: dict[Player, Attempt | None] = field(default_factory=_per_player(None))
    settings: Settings = field(default_factory=Settings)
    language: str = DEFAULT_LANGUAGE  # follows the phone's language (see ui/device_language.py)

    @property
    def lead(self) -> int:
        """How far the rope is pulled: positive towards LEFT, negative towards RIGHT."""
        return self.scores[Player.LEFT] - self.scores[Player.RIGHT]

    @property
    def winner(self) -> Player | None:
        """The player who is ``win_lead`` points ahead (the rope reached their end), if any."""
        if self.lead >= self.settings.win_lead:
            return Player.LEFT
        if -self.lead >= self.settings.win_lead:
            return Player.RIGHT
        return None

    @property
    def match_in_progress(self) -> bool:
        return self.screen in (Screen.COUNTDOWN, Screen.PLAYING)

    def reset(self):
        """Start over from the lobby. Settings and language are kept."""
        fresh = GameState()
        self.screen = fresh.screen
        self.countdown = fresh.countdown
        self.scores = fresh.scores
        self.problems = fresh.problems
        self.last_attempts = fresh.last_attempts
