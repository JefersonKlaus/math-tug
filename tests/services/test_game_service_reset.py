"""Responsibility: GameService.reset returns the game to the lobby."""

from unittest.mock import Mock

from math_tug.services.game_service import GameService
from math_tug.domain.player import Player
from math_tug.domain.state import GameState, Screen


def test_reset_restores_defaults_and_renders(state, rng):
    render = Mock()
    service = GameService(state, render, rng)
    state.screen = Screen.RESULT
    state.scores = {Player.LEFT: 5, Player.RIGHT: 3}
    state.problems[Player.LEFT] = service._new_problem(None)

    service.reset(None)

    assert state == GameState()
    render.assert_called_once_with()
