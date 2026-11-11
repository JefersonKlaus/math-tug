"""The column every screen is laid out in."""

import flet as ft

from ..layout import Layout


def screen_column(controls, layout: Layout, spacing_regular: int, spacing_compact: int, **kwargs):
    return ft.Column(controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=layout.pick(spacing_regular, spacing_compact), **kwargs)
