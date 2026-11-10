import flet as ft

from .config import BLUE, MUTED, PINK


def label(text: str, size: int = 10, color: str = MUTED):
    return ft.Text(
        text,
        size=size,
        color=color,
        font_family="monospace",
        weight=ft.FontWeight.W_500,
        letter_spacing=1.5,
    )


def avatar(initials: str, color: str, small: bool = False):
    size = 34 if small else 58
    return ft.Container(
        content=ft.Text(initials, size=10 if small else 16, weight=ft.FontWeight.BOLD),
        width=size,
        height=size,
        alignment=ft.alignment.center,
        border=ft.border.all(2, color),
        border_radius=size,
        bgcolor="#233D78" if color == BLUE else "#792754",
    )


def primary_button(text: str, on_click, height: int | None = None):
    return ft.ElevatedButton(text, on_click=on_click, bgcolor=PINK, color="white", height=height)
