"""Changing the settings."""

from collections.abc import Callable

from ..domain.state import GameState


class SettingsService:
    """Applies a change made on the settings screen and shows it."""

    def __init__(self, state: GameState, render: Callable[[], None]):
        self.state = state
        self.render = render

    def set_win_lead(self, value: int):
        self.state.settings.set_win_lead(value)
        self.render()

    def toggle_operation(self, operation: str):
        self.state.settings.toggle_operation(operation)
        self.render()

    def toggle_table(self, table: int):
        self.state.settings.toggle_table(table)
        self.render()
