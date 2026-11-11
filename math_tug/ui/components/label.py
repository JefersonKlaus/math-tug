"""A small monospace caption."""

import flet as ft

from ...theme import MUTED


def label(text: str, size: int = 10, color: str = MUTED):
    return ft.Text(
        text,
        size=size,
        color=color,
        font_family="monospace",
        weight=ft.FontWeight.W_500,
        style=ft.TextStyle(letter_spacing=1.5),
    )
