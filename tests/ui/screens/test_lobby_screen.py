"""Responsibility: LobbyScreen shows the LEFT vs RIGHT matchup and starts a match."""

from unittest.mock import Mock

import flet as ft

from math_tug.i18n import Translator
from math_tug.theme import BLUE, PINK
from math_tug.ui.layout import Layout
from math_tug.ui.screens.lobby import LobbyScreen
from tests.helpers import button_by_text, buttons, find_all, texts

EN = Translator()


def build(on_start=None, win_lead=3):
    return LobbyScreen(on_start or Mock(), win_lead, Layout(844, 390), EN).build()


def test_headline_is_centred():
    (headline,) = [c for c in build().controls if isinstance(c, ft.Row) and "tug?" in texts(c)]
    assert headline.alignment == ft.MainAxisAlignment.CENTER


def test_shows_left_blue_versus_right_pink():
    view = build()
    shown = texts(view)
    colours = {t.value: t.color for t in find_all(view, ft.Text) if t.value in ("LEFT", "RIGHT")}

    assert shown.index("LEFT") < shown.index("VS") < shown.index("RIGHT")
    assert colours == {"LEFT": BLUE, "RIGHT": PINK}


def test_states_the_chosen_points_ahead():
    assert "Get 5 points ahead to win the round" in texts(build(win_lead=5))


def test_single_start_button_wired_to_callback():
    on_start = Mock()
    view = build(on_start)

    assert len(buttons(view)) == 1
    assert button_by_text(view, "START MATCH").on_click is on_start
