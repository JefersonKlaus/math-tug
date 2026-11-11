"""A round badge with a player's initial."""

import flet as ft

from ...theme import BLUE


def avatar(initials: str, color: str, small: bool = False):
    size = 34 if small else 58
    return ft.Container(
        content=ft.Text(initials, size=10 if small else 16, weight=ft.FontWeight.BOLD),
        width=size,
        height=size,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(2, color),
        border_radius=size,
        bgcolor="#233D78" if color == BLUE else "#792754",
    )
