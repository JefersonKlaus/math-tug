"""Responsibility: the header shown on every screen (logo left, settings right)."""

from unittest.mock import Mock

from math_tug.ui.components.settings_button import settings_button
from math_tug.ui.header import fit_header, header
from math_tug.ui.layout import Layout
from tests.helpers import texts


def test_logo_left_and_settings_right():
    button = settings_button("SETTINGS", Mock())
    bar = header(button)

    assert texts(bar) == ["∑", "math", "tug"]        # no "LIVE MATCH", no player account
    assert bar.content.controls[-1] is button
    assert len(bar.content.controls) == 2


def test_is_slimmer_on_phones():
    bar = header(settings_button("SETTINGS", Mock()))
    fit_header(bar, Layout(568, 320))
    phone = bar.padding.top
    fit_header(bar, Layout(1024, 768))

    assert phone < bar.padding.top
