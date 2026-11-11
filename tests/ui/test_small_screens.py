"""Responsibility: every screen fits phones held sideways (nothing wider than the screen, compact sizes)."""

import random
from unittest.mock import Mock

import flet as ft
import pytest

from math_tug.i18n import Translator
from math_tug.services.game_service import GameService
from math_tug.ui.layout import Layout
from math_tug.domain.player import Player
from math_tug.ui.screens.countdown import CountdownScreen
from math_tug.ui.screens.game import GameScreen
from math_tug.ui.screens.lobby import LobbyScreen
from math_tug.ui.screens.result import ResultScreen
from math_tug.ui.screens.settings import SettingsScreen
from math_tug.domain.attempt import Attempt
from math_tug.domain.state import GameState
from tests.helpers import buttons, find_key, walk

SMALLEST_PHONE = Layout(568, 320)   # iPhone SE (1st gen) held sideways, the smallest common screen
SMALL_ANDROID = Layout(640, 360)
TABLET = Layout(1024, 768)

EN = Translator()


def finished_game():
    state = GameState()
    service = GameService(state, Mock(), random.Random(1))
    for player in Player:
        state.problems[player] = service._new_problem(None)
    problem = state.problems[Player.RIGHT]
    state.last_attempts[Player.RIGHT] = Attempt(problem, next(o for o in problem.options if o != problem.answer))
    state.scores = {Player.LEFT: 5, Player.RIGHT: 2}
    return state


def all_screens(layout):
    state = finished_game()
    return {
        "lobby": LobbyScreen(Mock(), 3, layout, EN).build(),
        "countdown": CountdownScreen(3, layout, EN).build(),
        "game": GameScreen(state, Mock(), Mock(), layout, EN).build(),
        "result": ResultScreen(state, Mock(), layout, EN).build(),
        "settings": SettingsScreen(state.settings, Mock(), Mock(), Mock(), Mock(), layout, EN).build(),
    }


@pytest.mark.parametrize("layout", [SMALLEST_PHONE, SMALL_ANDROID, TABLET], ids=["568x320", "640x360", "1024x768"])
def test_nothing_is_wider_than_the_screen(layout):
    for name, screen in all_screens(layout).items():
        too_wide = [c for c in walk(screen) if isinstance(getattr(c, "width", None), (int, float)) and c.width > layout.content_width]
        assert too_wide == [], f"{name}: {[type(c).__name__ + ' ' + str(c.width) for c in too_wide]}"


def test_phones_held_sideways_get_the_compact_sizes():
    state = finished_game()
    regular = GameScreen(state, Mock(), Mock(), TABLET, EN).build()
    compact = GameScreen(state, Mock(), Mock(), SMALLEST_PHONE, EN).build()

    def answer_height(view):
        return buttons(find_key(view, "panel-left"))[0].height

    assert answer_height(compact) < answer_height(regular)


def test_all_multiplication_tables_fit_one_row_on_the_smallest_phone():
    view = SettingsScreen(GameState().settings, Mock(), Mock(), Mock(), Mock(), SMALLEST_PHONE, EN).build()
    (row,) = [c for c in walk(find_key(view, "tables")) if isinstance(c, ft.Row)]

    assert sum(b.width for b in row.controls) + row.spacing * (len(row.controls) - 1) <= SMALLEST_PHONE.content_width

