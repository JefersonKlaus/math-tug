"""Responsibility: SettingsScreen shows the choices, highlights the current ones and reports taps."""

from unittest.mock import Mock

import pytest

from math_tug.i18n import Translator
from math_tug.theme import PINK
from math_tug.ui.layout import Layout
from math_tug.ui.screens.settings import SettingsScreen
from math_tug.domain.settings import Settings
from tests.helpers import button_by_text, button_labels, buttons, find_key, texts

EN = Translator()


@pytest.fixture
def settings():
    return Settings()


def build(settings, on_win_lead=None, on_toggle_operation=None, on_toggle_table=None, on_done=None):
    return SettingsScreen(settings, on_win_lead or Mock(), on_toggle_operation or Mock(), on_toggle_table or Mock(), on_done or Mock(), Layout(844, 390), EN).build()


def section(view, key):
    return buttons(find_key(view, key))


def selected(view, key):
    return [b.content for b in section(view, key) if b.bgcolor == PINK]


def test_shows_the_three_sections_with_their_choices_and_no_language(settings):
    view = build(settings)

    for title in ("POINTS AHEAD TO WIN", "OPERATIONS", "MULTIPLICATION TABLES  •  FOR × AND ÷"):
        assert title in texts(view)
    assert "LANGUAGE" not in texts(view)   # the language follows the phone
    assert button_labels(find_key(view, "points")) == ["3", "5", "7", "10"]
    assert button_labels(find_key(view, "operations")) == ["+", "-", "×", "÷"]
    assert button_labels(find_key(view, "tables")) == [str(n) for n in range(1, 11)]


def test_highlights_the_current_choices(settings):
    settings.set_win_lead(7)
    settings.toggle_operation("÷")
    settings.toggle_table(1)
    view = build(settings)

    assert selected(view, "points") == ["7"]
    assert selected(view, "operations") == ["+", "-", "×"]
    assert selected(view, "tables") == [str(n) for n in range(2, 11)]


def test_taps_report_what_was_tapped(settings):
    on_win_lead, on_operation, on_table = Mock(), Mock(), Mock()
    view = build(settings, on_win_lead, on_operation, on_table)

    next(b for b in section(view, "points") if b.content == "10").on_click(None)
    next(b for b in section(view, "operations") if b.content == "×").on_click(None)
    next(b for b in section(view, "tables") if b.content == "10").on_click(None)

    on_win_lead.assert_called_once_with(10)
    on_operation.assert_called_once_with("×")
    on_table.assert_called_once_with(10)


def test_tables_are_usable_while_divide_is_on(settings):
    settings.toggle_operation("×")
    assert not any(b.disabled for b in section(build(settings), "tables"))


def test_tables_are_disabled_without_times_and_divide(settings):
    settings.toggle_operation("×")
    settings.toggle_operation("÷")
    assert all(b.disabled for b in section(build(settings), "tables"))


def test_done_button_wired(settings):
    on_done = Mock()
    assert button_by_text(build(settings, on_done=on_done), "DONE").on_click is on_done
