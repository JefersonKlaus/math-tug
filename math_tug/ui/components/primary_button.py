"""The pink main button (Start, Play again, Done)."""

import flet as ft

from ...theme import PINK


def primary_button(text: str, on_click, height: int | None = None):
    return ft.Button(text, on_click=on_click, bgcolor=PINK, color="white", height=height)
