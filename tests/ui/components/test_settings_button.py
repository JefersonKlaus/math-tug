"""Responsibility: the Settings button in the header."""

from unittest.mock import Mock

import flet as ft

from math_tug.ui.components.settings_button import settings_button


def test_text_icon_and_handler():
    handler = Mock()
    button = settings_button("SETTINGS", handler)
    assert (button.content, button.icon, button.on_click) == ("SETTINGS", ft.Icons.SETTINGS, handler)
