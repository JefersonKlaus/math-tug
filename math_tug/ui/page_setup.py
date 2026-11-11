"""Window, theme and orientation."""

import flet as ft

from ..theme import BG


def configure_page(page: ft.Page):
    page.title = "Math Tug"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0
    page.window.width = 1200
    page.window.height = 700
    # Small enough to try the smallest phone held sideways (568 x 320) on a computer.
    page.window.min_width = 568
    page.window.min_height = 320
    page.window.resizable = True
    # On phones and tablets the app stays landscape, either way round (not supported on desktop or web).
    if page.platform.is_mobile() and not page.web:
        page.run_task(page.set_allowed_device_orientations, [ft.DeviceOrientation.LANDSCAPE_LEFT, ft.DeviceOrientation.LANDSCAPE_RIGHT])
