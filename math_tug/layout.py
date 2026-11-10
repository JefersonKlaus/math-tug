import flet as ft

from .config import BG, BLUE, PINK
from .components import avatar, label


def configure_page(page: ft.Page):
    page.title = "Math Tug"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0
    page.window.width = 1200
    page.window.height = 700
    page.window.min_width = 760
    page.window.min_height = 480
    page.window.resizable = True


def top_bar():
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=48, vertical=20),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(content=ft.Text("∑", size=19, color="white"), width=30, height=30, alignment=ft.alignment.center, bgcolor=PINK, border_radius=8),
                        ft.Text("math", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("tug", size=20, weight=ft.FontWeight.BOLD, color=PINK),
                    ],
                    spacing=0,
                ),
                ft.Row([ft.Container(width=7, height=7, bgcolor="#5EE3A1", border_radius=7), label("LIVE MATCH")], spacing=8),
                ft.Row([avatar("JD", BLUE, True), ft.Text("Jamie Doe", size=12, color="#D3D9EC"), ft.Text("⌄", size=17, color="#7885A8")], spacing=9),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )


def footer():
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=48, vertical=16),
        content=ft.Row(
            [label("© 2024 MATHTUG", 9), label("NO CALCULATORS. JUST BRAINS.", 9), label("v1.0.0", 9)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )
