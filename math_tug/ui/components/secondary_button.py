"""The outlined navy button (Settings, Restart, Keep playing)."""

import flet as ft

from ...theme import PANEL


def secondary_button(text: str, on_click, icon=None, height: int | None = None):
    """Outlined navy button; quieter than the pink primary button."""
    return ft.Button(
        text,
        icon=icon,
        on_click=on_click,
        height=height,
        bgcolor=PANEL,
        color="#D3D9EC",
        style=ft.ButtonStyle(side=ft.BorderSide(1, "#394A79")),
    )
