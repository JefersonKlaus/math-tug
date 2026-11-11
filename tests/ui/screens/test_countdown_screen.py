"""Responsibility: CountdownScreen displays the current countdown number."""

from math_tug.i18n import Translator
from math_tug.ui.layout import Layout
from math_tug.ui.screens.countdown import CountdownScreen
from tests.helpers import buttons, texts

EN = Translator()


def test_shows_the_number_and_instructions_without_buttons():
    view = CountdownScreen(2, Layout(844, 390), EN).build()

    assert texts(view) == ["GET READY", "2", "Eyes on the problem.", "Tap the right answer to pull the rope."]
    assert buttons(view) == []
