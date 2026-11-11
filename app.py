import flet as ft

from math_tug.app_controller import MathTugApp


async def main(page: ft.Page):
    await MathTugApp(page).start()


if __name__ == "__main__":
    ft.run(main)
