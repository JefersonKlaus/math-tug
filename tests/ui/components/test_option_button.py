"""Responsibility: an answer button shows its number and calls back when tapped."""

from unittest.mock import Mock

from math_tug.theme import BLUE
from math_tug.ui.components.option_button import option_button


def test_shows_the_number():
    handler = Mock()
    button = option_button(72, BLUE, handler, height=44)
    assert (button.content, button.on_click, button.height) == ("72", handler, 44)
