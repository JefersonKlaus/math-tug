"""Responsibility: MathTugApp.render picks the right screen, sizes it for the screen and updates it in place."""

import flet as ft
import pytest

from math_tug.app_controller import MathTugApp
from math_tug.ui.layout import Layout
from math_tug.domain.player import Player
from math_tug.domain.state import Screen
from tests.helpers import button_by_text, buttons, find_key, texts, walk


@pytest.fixture
def app(page):
    app = MathTugApp(page)
    for player in Player:
        app.state.problems[player] = app.game._new_problem(None)
    return app


def rendered(app, screen):
    app.state.screen = screen
    app.render()
    return app.content.content


def test_lobby(app):
    view = rendered(app, Screen.LOBBY)
    assert button_by_text(view, "START MATCH").on_click == app.game.start_match


def test_countdown(app):
    app.state.countdown = 2
    assert texts(rendered(app, Screen.COUNTDOWN))[:2] == ["GET READY", "2"]


def test_playing_routes_answers_and_restart_to_the_game(app):
    view = rendered(app, Screen.PLAYING)
    problem = app.state.problems[Player.LEFT]

    buttons(find_key(view, "panel-left"))[problem.options.index(problem.answer)].on_click(None)

    assert app.state.scores[Player.LEFT] == 1
    assert button_by_text(view, "RESTART GAME").on_click == app.game.restart


def test_result(app):
    app.state.scores[Player.RIGHT] = 3
    view = rendered(app, Screen.RESULT)

    assert "RIGHT wins!" in texts(view)
    assert button_by_text(view, "PLAY AGAIN").on_click == app.game.reset


def test_settings(app):
    view = rendered(app, Screen.SETTINGS)
    assert button_by_text(view, "DONE").on_click == app.game.close_settings


def test_answering_keeps_the_other_players_buttons(app, page):
    """A tap from the other player may already be on its way to these exact buttons."""
    view = rendered(app, Screen.PLAYING)
    right_buttons = buttons(find_key(view, "panel-right"))
    problem = app.state.problems[Player.LEFT]

    buttons(find_key(view, "panel-left"))[problem.options.index(problem.answer)].on_click(None)

    assert app.content.content is view  # screen updated in place, not replaced
    assert all(a is b for a, b in zip(buttons(find_key(view, "panel-right")), right_buttons))
    assert app.state.problems[Player.LEFT].expression in texts(view)
    assert page.update_calls == 2


def test_new_match_gets_a_fresh_playing_screen(app):
    first = rendered(app, Screen.PLAYING)
    app.state.scores[Player.LEFT] = 3
    rendered(app, Screen.RESULT)
    app.state.scores[Player.LEFT] = 0

    assert rendered(app, Screen.PLAYING) is not first


@pytest.mark.parametrize("screen", [Screen.LOBBY, Screen.SETTINGS, Screen.RESULT])
def test_screens_can_scroll_so_no_button_is_out_of_reach(app, screen):
    app.state.scores[Player.LEFT] = 3 if screen is Screen.RESULT else 0
    assert rendered(app, screen).scroll == ft.ScrollMode.AUTO


def test_the_game_fills_the_screen_instead_of_scrolling(app):
    """Its panels stretch to the height that is left, which a scrolling view would break."""
    view = rendered(app, Screen.PLAYING)
    assert isinstance(view, ft.Container) and view.expand is True
    assert not any(getattr(c, "scroll", None) for c in walk(view))


def test_resizing_rebuilds_the_screen_for_the_new_size(app, page):
    app.run()
    view = rendered(app, Screen.PLAYING)
    phone_header = app.header.padding.top
    assert find_key(view, "panel-left").padding.left == Layout(844, 390).pick(20, 8)

    page.width, page.height = 1200, 700   # e.g. the window is made bigger
    page.on_resize(None)  # what Flet calls when the window or screen size changes

    assert find_key(app.content.content, "panel-left").padding.left == Layout(1200, 700).pick(20, 8)
    assert app.header.padding.top > phone_header   # header and footer follow the size too
