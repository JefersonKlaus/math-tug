"""The Restart game button under the game."""

import flet as ft

from .secondary_button import secondary_button


def restart_button(text: str, on_click, height: int = 36):
    # Secondary style, so it is less likely to be tapped by accident than the pink buttons.
    return secondary_button(text, on_click, ft.Icons.RESTART_ALT, height)
