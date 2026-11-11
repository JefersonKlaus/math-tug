"""Responsibility: the settings button always works and asks before ending a running game."""

import asyncio

import pytest

from math_tug.app_controller import MathTugApp
from math_tug.domain.player import Player
from math_tug.domain.state import Screen
from tests.helpers import button_by_text, texts

LEFT = Player.LEFT


@pytest.fixture
def app(page, no_sleep):
    app = MathTugApp(page)
    app.run()
    return app


@pytest.fixture
def playing(app):
    asyncio.run(app.game.start_match(None))
    problem = app.state.problems[LEFT]
    app.game.choose_answer(LEFT, problem, problem.answer)  # 1-0
    return app


def press_settings(app):
    app.settings_button.on_click(None)


def action(dialog, label):
    return button_by_text(dialog.content, label)


@pytest.mark.parametrize("screen", [Screen.LOBBY, Screen.RESULT])
def test_opens_settings_straight_away_when_no_game_is_running(app, page, screen):
    app.state.screen = screen
    app.state.scores[LEFT] = 3 if screen is Screen.RESULT else 0

    press_settings(app)

    assert page.dialogs == []
    assert app.state.screen is Screen.SETTINGS


@pytest.mark.parametrize("screen", [Screen.COUNTDOWN, Screen.PLAYING])
def test_during_a_game_asks_first(playing, page, screen):
    playing.state.screen = screen

    press_settings(playing)

    assert page.open_dialog is playing.settings_opener.dialog
    assert playing.state.screen is screen     # nothing ended yet
    assert playing.state.scores[LEFT] == 1


def test_keep_playing_closes_the_popup_and_the_game_goes_on(playing, page):
    press_settings(playing)

    action(page.open_dialog, "KEEP PLAYING").on_click(None)

    assert page.open_dialog is None
    assert playing.state.screen is Screen.PLAYING
    assert playing.state.scores[LEFT] == 1


def test_end_game_closes_the_popup_and_opens_settings(playing, page):
    press_settings(playing)

    action(page.open_dialog, "END GAME").on_click(None)

    assert page.open_dialog is None
    assert playing.state.scores == {Player.LEFT: 0, Player.RIGHT: 0}
    assert "POINTS AHEAD TO WIN" in texts(playing.content)


def test_double_tap_opens_one_popup(playing, page):
    press_settings(playing)
    press_settings(playing)

    assert len(page.dialogs) == 1


def test_can_ask_again_right_after_keep_playing(playing, page):
    """Flet keeps a closed dialog attached for its closing animation; asking again must still work."""
    press_settings(playing)
    action(page.open_dialog, "KEEP PLAYING").on_click(None)

    press_settings(playing)

    assert page.open_dialog is playing.settings_opener.dialog
