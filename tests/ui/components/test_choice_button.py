"""Responsibility: a settings choice shows whether it is selected or disabled."""

from unittest.mock import Mock

import flet as ft

from math_tug.theme import PANEL, PINK
from math_tug.ui.components.choice_button import choice_button


def test_is_filled_only_when_selected():
    assert choice_button("7", True, Mock()).bgcolor == PINK
    assert choice_button("7", False, Mock()).bgcolor == PANEL


def test_disabled_is_dimmed():
    button = choice_button("7", True, Mock(), enabled=False)
    assert button.disabled is True
    assert button.opacity < 1.0


def test_has_no_inner_padding_so_two_digits_fit():
    assert choice_button("10", True, Mock(), width=54).style.padding == ft.Padding.all(0)
