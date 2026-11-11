"""Responsibility: SettingsService applies a change made on the settings screen and shows it."""

from unittest.mock import Mock

from math_tug.services.settings_service import SettingsService


def test_changes_update_the_settings_and_the_screen(state):
    render = Mock()
    service = SettingsService(state, render)

    service.set_win_lead(10)
    service.toggle_operation("×")
    service.toggle_table(3)

    assert state.settings.win_lead == 10
    assert "×" not in state.settings.operations
    assert 3 not in state.settings.tables
    assert render.call_count == 3
