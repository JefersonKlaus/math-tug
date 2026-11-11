"""Responsibility: the popup that asks before settings end a running game."""

from unittest.mock import Mock

from math_tug.i18n import Translator
from math_tug.theme import PANEL, PINK
from math_tug.ui.components.end_game_dialog import end_game_dialog
from tests.helpers import buttons, texts

EN = Translator()


def test_is_modal_and_says_the_game_will_end():
    dialog = end_game_dialog(EN, Mock(), Mock())
    assert dialog.modal is True
    assert texts(dialog.title) == ["SETTINGS", "End the game?"]
    assert texts(dialog.content)[0] == "Opening settings will finish the current game."


def test_follows_the_app_design():
    dialog = end_game_dialog(EN, Mock(), Mock())
    assert dialog.shape.side.color == PINK
    keep, end = buttons(dialog.content)
    assert keep.bgcolor == PANEL   # secondary (outlined) style, like Settings and Restart
    assert end.bgcolor == PINK     # primary style, like Start and Play again


def test_keep_playing_and_end_game_actions():
    on_keep, on_end = Mock(), Mock()
    keep, end = buttons(end_game_dialog(EN, on_keep, on_end).content)
    assert (keep.content, keep.on_click) == ("KEEP PLAYING", on_keep)
    assert (end.content, end.on_click) == ("END GAME", on_end)


def test_scrolls_if_it_does_not_fit():
    assert end_game_dialog(EN, Mock(), Mock()).scrollable is True
