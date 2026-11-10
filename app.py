import flet as ft

from math_tug.app_controller import MathTugApp


def main(page: ft.Page):
    MathTugApp(page).run()


if __name__ == "__main__":
    ft.app(target=main)
