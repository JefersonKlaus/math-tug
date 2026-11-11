"""Responsibility: Layout turns the screen size into the sizes the landscape UI is built with."""

import pytest

from math_tug.ui.layout import Layout
from tests.helpers import FakePage


def test_reads_the_page_size():
    assert Layout.of(FakePage(width=640, height=360)) == Layout(640, 360)


def test_falls_back_to_the_window_size_before_the_page_knows_its_size():
    assert Layout.of(FakePage(width=None, height=None)) == Layout(1200, 700)


@pytest.mark.parametrize("height, compact", [(320, True), (430, True), (599, True), (600, False), (768, False)])
def test_phones_held_sideways_are_compact(height, compact):
    assert Layout(900, height).compact is compact


def test_pick_chooses_the_size_for_the_screen():
    assert Layout(1200, 700).pick("regular", "compact") == "regular"
    assert Layout(568, 320).pick("regular", "compact") == "compact"


def test_content_fills_the_width_minus_the_padding():
    assert Layout(568, 320).content_width == 568 - 2 * 8
    assert Layout(1024, 768).content_width == 1024 - 2 * 20


def test_content_keeps_its_shape_on_very_wide_screens():
    assert Layout(1920, 1080).content_width == 1100 - 2 * 20
