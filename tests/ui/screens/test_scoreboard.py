"""Responsibility: the scoreboard (sides, scores and rope) shown during and after play."""

import flet as ft
import pytest

from math_tug.i18n import Translator
from math_tug.ui.components.tug_bar import knot_left
from math_tug.ui.layout import Layout
from math_tug.domain.player import Player
from math_tug.ui.screens.scoreboard import scoreboard
from tests.helpers import find_all, texts

EN = Translator()


def test_left_player_then_rope_then_right_player(state, layout):
    state.scores = {Player.LEFT: 3, Player.RIGHT: 1}

    assert texts(scoreboard(state, layout, EN)) == ["L", "LEFT", "3", "3 POINTS AHEAD WINS", "1", "RIGHT", "R"]


def test_states_the_chosen_points_ahead(state, layout):
    state.settings.set_win_lead(10)

    assert "10 POINTS AHEAD WINS" in texts(scoreboard(state, layout, EN))


def test_rope_follows_the_lead(state, layout):
    state.scores = {Player.LEFT: 1, Player.RIGHT: 3}
    (bar,) = find_all(scoreboard(state, layout, EN), ft.Stack)

    assert bar.controls[-1].left == pytest.approx(knot_left(-2, 3, bar.width))


def test_rope_is_at_most_460_wide(state):
    (bar,) = find_all(scoreboard(state, Layout(1200, 700), EN), ft.Stack)
    assert bar.width == 460


def test_rope_leaves_room_for_longer_names_on_small_phones(state):
    small = Layout(568, 320)
    (english,) = find_all(scoreboard(state, small, EN), ft.Stack)
    (portuguese,) = find_all(scoreboard(state, small, Translator("pt")), ft.Stack)

    assert portuguese.width < english.width < small.content_width
