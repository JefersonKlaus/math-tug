"""Responsibility: GameState defaults, derived queries (lead, winner, match in progress) and reset."""

import random

import pytest

from math_tug.domain.problem import make_problem
from math_tug.domain.attempt import Attempt
from math_tug.domain.state import GameState, Screen
from math_tug.domain.player import Player

LEFT, RIGHT = Player.LEFT, Player.RIGHT


def test_defaults(state):
    assert state.screen is Screen.LOBBY
    assert state.language == "en"
    assert state.scores == {LEFT: 0, RIGHT: 0}
    assert state.problems == {LEFT: None, RIGHT: None}
    assert state.last_attempts == {LEFT: None, RIGHT: None}


@pytest.mark.parametrize("left, right, lead", [(0, 0, 0), (2, 0, 2), (0, 3, -3)])
def test_lead_is_left_minus_right(state, left, right, lead):
    state.scores = {LEFT: left, RIGHT: right}
    assert state.lead == lead


@pytest.mark.parametrize("left, right, winner", [
    (3, 0, LEFT),     # default: 3 points ahead wins
    (10, 7, LEFT),
    (2, 5, RIGHT),
    (4, 2, None),     # only 2 ahead
    (5, 5, None),
])
def test_winner_is_the_player_three_points_ahead(state, left, right, winner):
    state.scores = {LEFT: left, RIGHT: right}
    assert state.winner is winner


def test_winner_follows_the_chosen_points_ahead(state):
    state.settings.set_win_lead(5)
    state.scores = {LEFT: 9, RIGHT: 5}
    assert state.winner is None
    state.scores[LEFT] = 10                # the example: 10 against 5
    assert state.winner is LEFT


@pytest.mark.parametrize("screen, in_progress", [
    (Screen.LOBBY, False), (Screen.COUNTDOWN, True), (Screen.PLAYING, True), (Screen.RESULT, False), (Screen.SETTINGS, False),
])
def test_match_in_progress(state, screen, in_progress):
    state.screen = screen
    assert state.match_in_progress is in_progress


def test_reset_restores_the_defaults_but_keeps_the_settings(state):
    problem = make_problem(random.Random(1))
    settings = state.settings
    settings.set_win_lead(10)
    state.language = "pt"
    state.screen = Screen.RESULT
    state.scores = {LEFT: 5, RIGHT: 2}
    state.problems[LEFT] = problem
    state.last_attempts[RIGHT] = Attempt(problem, 0)

    state.reset()

    assert state.settings is settings and settings.win_lead == 10
    assert state.language == "pt"
    state.settings, state.language = GameState().settings, "en"
    assert state == GameState()
