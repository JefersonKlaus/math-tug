"""The Settings button: it always works, but asks first if a game is running."""

from collections.abc import Callable

import flet as ft

from ..domain.state import GameState
from ..i18n import Translator
from ..services.game_service import GameService
from .components.end_game_dialog import end_game_dialog


class SettingsOpener:
    def __init__(self, page: ft.Page, state: GameState, game: GameService, translator: Callable[[], Translator]):
        self.page = page
        self.state = state
        self.game = game
        self.translator = translator
        self.dialog: ft.AlertDialog | None = None
        self._dialogs_shown = 0

    def on_click(self, _):
        if not self.state.match_in_progress:
            self.game.open_settings(None)
            return
        if self.dialog is not None and self.dialog.open:
            return  # already asking (double tap)
        # A new dialog each time: Flet keeps a closed dialog attached until its
        # closing animation ends, and showing that same one again would fail.
        # Flet checks "already shown" with ==, and controls compare by value;
        # a unique `data` keeps each dialog distinct without relying on Flet
        # internals (today Flet's own on_dismiss wrapper happens to differ too).
        self._dialogs_shown += 1
        self.dialog = end_game_dialog(self.translator(), self._keep_playing, self._end_game_and_open_settings)
        self.dialog.data = self._dialogs_shown
        self.page.show_dialog(self.dialog)

    def _keep_playing(self, _):
        self.page.pop_dialog()

    def _end_game_and_open_settings(self, _):
        self.page.pop_dialog()
        self.game.open_settings(None)
