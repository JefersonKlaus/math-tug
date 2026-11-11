"""Responsibility: GameService goes to and from settings, and new problems follow the settings."""

import asyncio
from unittest.mock import Mock

import pytest

from math_tug.services.game_service import GameService
from math_tug.domain.player import Player
from math_tug.domain.state import Screen


@pytest.fixture
def render():
    return Mock()


@pytest.fixture
def service(state, render, rng):
    return GameService(state, render, rng)


@pytest.mark.parametrize("screen", [Screen.LOBBY, Screen.RESULT, Screen.PLAYING])
def test_opening_settings_ends_any_game(service, state, render, screen):
    """During a game the app asks first (see test_app_settings_dialog); the service just ends it."""
    state.screen = screen
    state.scores[Player.LEFT] = 2

    service.open_settings(None)

    assert state.screen is Screen.SETTINGS
    assert state.scores[Player.LEFT] == 0
    render.assert_called_once_with()


def test_done_returns_to_the_lobby(service, state, render):
    state.screen = Screen.SETTINGS

    service.close_settings(None)

    assert state.screen is Screen.LOBBY
    render.assert_called_once_with()


def test_new_problems_only_use_chosen_operations(service, state, no_sleep):
    for op in ("-", "×", "÷"):
        state.settings.toggle_operation(op)
    asyncio.run(service.start_match(None))

    for _ in range(30):
        problem = state.problems[Player.LEFT]
        assert " + " in problem.expression
        service.choose_answer(Player.LEFT, problem, next(o for o in problem.options if o != problem.answer))


def test_new_problems_only_use_chosen_tables(service, state, no_sleep):
    state.settings.toggle_operation("+")
    state.settings.toggle_operation("-")
    for n in (1, 2, 3, 4, 5, 6, 7, 9, 10):
        state.settings.toggle_table(n)                 # only the 8 table
    asyncio.run(service.start_match(None))

    for _ in range(30):
        problem = state.problems[Player.LEFT]
        left, symbol, right = problem.expression.split()
        assert (left if symbol == "×" else right) == "8"
        service.choose_answer(Player.LEFT, problem, next(o for o in problem.options if o != problem.answer))
