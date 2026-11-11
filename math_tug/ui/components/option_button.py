"""One of the three answer buttons."""

import flet as ft


def option_button(value: int, color: str, on_click, height: int = 56, text_size: int = 28):
    """A big answer button; the three of a panel share its width."""
    return ft.Button(
        str(value),
        on_click=on_click,
        expand=True,
        height=height,
        bgcolor="#2A3B6B",
        color="white",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=text_size, weight=ft.FontWeight.BOLD),
            shape=ft.RoundedRectangleBorder(radius=16),
            side=ft.BorderSide(2, color),
        ),
    )
