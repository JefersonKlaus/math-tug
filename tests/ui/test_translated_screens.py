"""Responsibility: in Portuguese, no screen still shows English text (nothing was left untranslated)."""

import random
from unittest.mock import Mock

import pytest

from math_tug.ui.components.end_game_dialog import end_game_dialog
from math_tug.services.game_service import GameService
from math_tug.i18n import Translator, en, pt
from math_tug.ui.layout import Layout
from math_tug.domain.player import Player
from math_tug.ui.screens.countdown import CountdownScreen
from math_tug.ui.screens.game import GameScreen
from math_tug.ui.screens.lobby import LobbyScreen
from math_tug.ui.screens.result import ResultScreen
from math_tug.ui.screens.settings import SettingsScreen
from math_tug.domain.attempt import Attempt
from math_tug.domain.state import GameState
from tests.helpers import button_labels, texts

PT = Translator("pt")
# English texts that are different in Portuguese ("VS" is the same in both).
ENGLISH_ONLY = {text for key, text in en.STRINGS.items() if text != pt.STRINGS[key]}
ENGLISH_WORDS = {"LEFT", "RIGHT", "TAP", "ANSWER", "POINTS", "AHEAD", "WINS", "wins", "Nice", "Oops", "RESTART", "GAME", "MATCH", "SETTINGS", "Settings", "DONE", "PLAY", "AGAIN"}


def game_with_feedback():
    state = GameState()
    service = GameService(state, Mock(), random.Random(1))
    for player in Player:
        state.problems[player] = service._new_problem(None)
    for player, correct in ((Player.LEFT, True), (Player.RIGHT, False)):
        problem = state.problems[player]
        state.last_attempts[player] = Attempt(problem, problem.answer if correct else next(o for o in problem.options if o != problem.answer))
    state.scores = {Player.LEFT: 3, Player.RIGHT: 0}
    return state


def portuguese_screens():
    state, layout = game_with_feedback(), Layout(844, 390)
    return {
        "lobby": LobbyScreen(Mock(), 3, layout, PT).build(),
        "countdown": CountdownScreen(3, layout, PT).build(),
        "game": GameScreen(state, Mock(), Mock(), layout, PT).build(),
        "result": ResultScreen(state, Mock(), layout, PT).build(),
        "settings": SettingsScreen(state.settings, Mock(), Mock(), Mock(), Mock(), layout, PT).build(),
        "popup": end_game_dialog(PT, Mock(), Mock()),
    }


@pytest.mark.parametrize("name", ["lobby", "countdown", "game", "result", "settings", "popup"])
def test_no_english_left(name):
    screen = portuguese_screens()[name]
    shown = texts(screen) + button_labels(screen)
    if name == "popup":
        shown += texts(screen.title)

    assert [s for s in shown if s in ENGLISH_ONLY] == []
    assert [s for s in shown if set(s.replace("!", " ").replace("•", " ").split()) & ENGLISH_WORDS] == []
