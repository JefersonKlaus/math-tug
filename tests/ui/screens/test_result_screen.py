"""Responsibility: ResultScreen announces the winner and offers a replay."""

from unittest.mock import Mock

import flet as ft
import pytest

from math_tug.i18n import Translator
from math_tug.ui.layout import Layout
from math_tug.domain.player import Player
from math_tug.theme import PLAYER_COLORS
from math_tug.ui.screens.result import ResultScreen
from tests.helpers import button_by_text, button_labels, find_all, texts

EN = Translator()


@pytest.mark.parametrize("scores, winner", [((8, 3), Player.LEFT), ((2, 7), Player.RIGHT)])
def test_announces_the_winner_in_their_colour(state, scores, winner):
    state.scores = dict(zip(Player, scores))
    view = ResultScreen(state, Mock(), Layout(844, 390), EN).build()

    (title,) = [t for t in find_all(view, ft.Text) if t.value.endswith("wins!")]
    assert title.value == f"{EN(f'player.{winner.value}')} wins!"
    assert title.color == PLAYER_COLORS[winner]
    assert f"Final score {scores[0]} – {scores[1]}" in texts(view)


def test_play_again_button_wired_to_reset(state):
    state.scores = {Player.LEFT: 3, Player.RIGHT: 0}
    on_reset = Mock()
    view = ResultScreen(state, on_reset, Layout(844, 390), EN).build()

    assert button_labels(view) == ["PLAY AGAIN  →"]
    assert button_by_text(view, "PLAY AGAIN").on_click is on_reset
