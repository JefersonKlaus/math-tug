"""Responsibility: complete games played through the on-screen buttons, end to end."""

import asyncio
import random

import pytest

from math_tug.app_controller import MathTugApp
from math_tug.config import WIN_LEAD
from math_tug.domain.player import Player
from math_tug.domain.state import GameState, Screen
from tests.helpers import FakePage, app_parts, button_by_text, buttons, find_key, texts

LEFT, RIGHT = Player.LEFT, Player.RIGHT


@pytest.fixture
def app(page, no_sleep):
    app = MathTugApp(page)
    app.game.rng = random.Random(42)
    app.run()
    return app


def click(app, fragment):
    result = button_by_text(app.content, fragment).on_click(None)
    if asyncio.iscoroutine(result):
        asyncio.run(result)


def tap_option(app, player, correct=True):
    problem = app.state.problems[player]
    panel = find_key(app.content, f"panel-{player.value}")
    labels = [b.content for b in buttons(panel)]
    value = problem.answer if correct else next(o for o in problem.options if o != problem.answer)
    buttons(panel)[labels.index(str(value))].on_click(None)


def setting(app, key, label):
    (button,) = [b for b in buttons(find_key(app.content, key)) if b.content == label]
    button.on_click(None)


def test_lobby_to_result_and_back(app):
    click(app, "START MATCH")
    for _ in range(WIN_LEAD):
        tap_option(app, LEFT)

    assert "LEFT wins!" in texts(app.content)
    assert f"Final score {WIN_LEAD} – 0" in texts(app.content)

    click(app, "PLAY AGAIN")
    assert app.state == GameState()
    assert "Ready to " in texts(app.content)


def test_close_game_goes_on_until_someone_is_five_ahead(app):
    app.state.settings.set_win_lead(5)
    click(app, "START MATCH")

    for _ in range(5):
        tap_option(app, LEFT)
        tap_option(app, RIGHT)                   # 5-5
    for _ in range(4):
        tap_option(app, RIGHT)                   # 5-9
    assert app.state.screen is Screen.PLAYING

    tap_option(app, RIGHT)                       # 5-10

    assert "RIGHT wins!" in texts(app.content)
    assert "Final score 5 – 10" in texts(app.content)


def test_restart_button_starts_the_game_over(app):
    click(app, "START MATCH")
    tap_option(app, LEFT)
    tap_option(app, RIGHT, correct=False)

    click(app, "RESTART GAME")

    assert app.state.screen is Screen.PLAYING
    assert app.state.scores == {LEFT: 0, RIGHT: 0}
    assert "Oops" not in " ".join(texts(app.content))


def test_configure_then_play_an_addition_only_round(app):
    app.settings_button.on_click(None)
    for op in ("-", "×", "÷"):
        setting(app, "operations", op)
    click(app, "DONE")

    click(app, "START MATCH")
    for _ in range(WIN_LEAD):
        assert " + " in app.state.problems[LEFT].expression
        tap_option(app, LEFT)

    assert "LEFT wins!" in texts(app.content)


def test_practise_only_the_seven_times_table(app):
    app.settings_button.on_click(None)
    for op in ("+", "-"):
        setting(app, "operations", op)
    for n in (1, 2, 3, 4, 5, 6, 8, 9, 10):
        setting(app, "tables", str(n))
    click(app, "DONE")
    click(app, "START MATCH")

    for _ in range(WIN_LEAD):
        left, symbol, right = app.state.problems[RIGHT].expression.split()
        assert (left if symbol == "×" else right) == "7"
        tap_option(app, RIGHT)

    assert "RIGHT wins!" in texts(app.content)


def test_a_portuguese_phone_plays_in_portuguese(no_sleep):
    page = FakePage(languages=("pt",))
    app = MathTugApp(page)
    app.game.rng = random.Random(42)
    asyncio.run(app.start())

    _, _, footer = app_parts(page)
    assert "Prontos para " in texts(app.content)
    assert app.settings_button.content == "CONFIGURAÇÕES"
    assert "SEM CALCULADORA. SÓ CÉREBRO." in texts(footer)

    click(app, "COMEÇAR PARTIDA")
    for _ in range(WIN_LEAD):
        tap_option(app, LEFT)

    assert "ESQUERDA venceu!" in texts(app.content)
