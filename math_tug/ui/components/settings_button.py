"""The Settings button in the header."""

import flet as ft

from .secondary_button import secondary_button


def settings_button(text: str, on_click):
    return secondary_button(text, on_click, ft.Icons.SETTINGS, 34)
