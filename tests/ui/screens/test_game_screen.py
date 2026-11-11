"""Responsibility: GameScreen during play (one panel per player, feedback, restart button, in-place refresh)."""

from unittest.mock import Mock

import flet as ft
import pytest

from math_tug.i18n import Translator
from math_tug.theme import GREEN, RED
from math_tug.services.game_service import GameService
from math_tug.ui.layout import Layout
from math_tug.domain.player import Player
from math_tug.theme import PLAYER_COLORS
from math_tug.ui.screens.game import GameScreen
from math_tug.domain.attempt import Attempt
from math_tug.domain.state import Screen
from tests.helpers import button_labels, buttons, find_all, find_key, texts

EN = Translator()


@pytest.fixture
def playing(state, rng):
    service = GameService(state, Mock(), rng)
    for player in Player:
        state.problems[player] = service._new_problem(None)
    state.screen = Screen.PLAYING
    return state


def build(state, on_choose=None, on_restart=None):
    return GameScreen(state, on_choose or Mock(), on_restart or Mock(), Layout(844, 390), EN).build()


def panel(view, player):
    return find_key(view, f"panel-{player.value}")


def test_left_panel_then_right_panel(playing):
    row = next(c for c in build(playing).controls if isinstance(c, ft.Row))
    assert [p.key for p in row.controls] == ["panel-left", "panel-right"]


@pytest.mark.parametrize("player", list(Player))
def test_panel_shows_that_players_problem_and_three_answers(playing, player):
    view = panel(build(playing), player)
    problem = playing.problems[player]

    assert view.border.top.color == PLAYER_COLORS[player]
    assert f"{EN(f'player.{player.value}')}  •  TAP THE ANSWER" in texts(view)
    assert problem.expression in texts(view)
    assert button_labels(view) == [str(o) for o in problem.options]


@pytest.mark.parametrize("player", list(Player))
def test_tapping_an_answer_reports_player_problem_and_value(playing, player):
    on_choose = Mock()
    problem = playing.problems[player]

    buttons(panel(build(playing, on_choose), player))[1].on_click(None)

    on_choose.assert_called_once_with(player, problem, problem.options[1])


def test_correct_feedback(playing):
    problem = playing.problems[Player.LEFT]
    playing.last_attempts[Player.LEFT] = Attempt(problem, problem.answer)

    left = panel(build(playing), Player.LEFT)

    assert "Nice! +1" in texts(left)
    assert [i.color for i in find_all(left, ft.Icon)] == [GREEN]


def test_wrong_feedback_shows_the_right_answer(playing):
    problem = playing.problems[Player.RIGHT]
    playing.last_attempts[Player.RIGHT] = Attempt(problem, next(o for o in problem.options if o != problem.answer))

    right = panel(build(playing), Player.RIGHT)

    assert f"Oops! {problem.expression} = {problem.answer}" in texts(right)
    assert [i.color for i in find_all(right, ft.Icon)] == [RED]


def test_restart_button_is_below_the_game_in_the_centre(playing):
    on_restart = Mock()
    view = build(playing, on_restart=on_restart)
    restart = view.controls[-1]

    assert (restart.content, restart.on_click) == ("RESTART GAME", on_restart)
    assert view.horizontal_alignment == ft.CrossAxisAlignment.CENTER


class TestRefreshInPlace:
    """Rebuilding a panel would drop the other player's in-flight tap, so only changed panels rebuild."""

    def test_refresh_rebuilds_only_the_panel_that_changed(self, playing):
        screen = GameScreen(playing, Mock(), Mock(), Layout(844, 390), EN)
        view = screen.build()
        left_before = panel(view, Player.LEFT).content
        right_before = panel(view, Player.RIGHT).content
        problem = playing.problems[Player.LEFT]
        playing.last_attempts[Player.LEFT] = Attempt(problem, problem.answer)

        screen.refresh()

        assert panel(view, Player.LEFT).content is not left_before
        assert panel(view, Player.RIGHT).content is right_before

    def test_refresh_updates_the_scoreboard(self, playing):
        screen = GameScreen(playing, Mock(), Mock(), Layout(844, 390), EN)
        view = screen.build()
        playing.scores[Player.RIGHT] = 4

        screen.refresh()

        assert "4" in texts(view)
