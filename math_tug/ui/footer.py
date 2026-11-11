"""The bar at the bottom of every screen."""

import flet as ft

from .components.label import label
from .layout import Layout


def footer(tagline: ft.Text):
    return ft.Container(
        content=ft.Row(
            [label("© 2024 MATHTUG", 9), tagline, label("v1.0.0", 9)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )


def fit_footer(footer_bar: ft.Container, layout: Layout):
    """Less height on short screens."""
    footer_bar.padding = ft.Padding.symmetric(horizontal=layout.pick(48, 16), vertical=layout.pick(14, 4))
