"""The bar at the top of every screen."""

import flet as ft

from ..theme import PINK
from .layout import Layout


def header(settings_control: ft.Control):
    """The logo on the left and the settings button on the right."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(content=ft.Text("∑", size=19, color="white"), width=30, height=30, alignment=ft.Alignment.CENTER, bgcolor=PINK, border_radius=8),
                        ft.Text("math", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("tug", size=20, weight=ft.FontWeight.BOLD, color=PINK),
                    ],
                    spacing=0,
                ),
                settings_control,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )


def fit_header(header_bar: ft.Container, layout: Layout):
    """Less height on short screens."""
    header_bar.padding = ft.Padding.symmetric(horizontal=layout.pick(48, 16), vertical=layout.pick(16, 4))
