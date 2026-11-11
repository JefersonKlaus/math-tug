"""Responsibility: the footer shown on every screen."""

import flet as ft

from math_tug.ui.footer import fit_footer, footer
from math_tug.ui.layout import Layout
from tests.helpers import texts


def test_copyright_tagline_and_version():
    assert texts(footer(ft.Text("TAGLINE"))) == ["© 2024 MATHTUG", "TAGLINE", "v1.0.0"]


def test_is_slimmer_on_phones():
    bar = footer(ft.Text("TAGLINE"))
    fit_footer(bar, Layout(568, 320))
    phone = bar.padding.top
    fit_footer(bar, Layout(1024, 768))

    assert phone < bar.padding.top
