"""A choice on the settings screen."""

import flet as ft

from ...theme import PANEL, PINK


def choice_button(text: str, selected: bool, on_click, width: int = 64, enabled: bool = True, height: int = 52, text_size: int = 22):
    """A setting choice; the selected one is filled, the others are outlined."""
    return ft.Button(
        text,
        on_click=on_click,
        disabled=not enabled,
        opacity=1.0 if enabled else 0.35,
        width=width,
        height=height,
        bgcolor=PINK if selected else PANEL,
        color="white" if selected else "#D3D9EC",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=text_size, weight=ft.FontWeight.BOLD),
            padding=ft.Padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=14),
            side=ft.BorderSide(2, PINK if selected else "#394A79"),
        ),
    )
