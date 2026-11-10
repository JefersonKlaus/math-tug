import flet as ft

from .components import label
from .game_service import GameService
from .layout import configure_page, footer, top_bar
from .screens import CountdownScreen, GameScreen, LobbyScreen
from .state import GameState, Screen


class MathTugApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = GameState()
        self.content = ft.Container(expand=True)
        self.answer = ft.TextField(width=125, text_size=48, color="#65B5FF", border_color="#65B5FF", border_width=0, focused_border_width=0, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER, on_submit=self._submit_from_field)
        self.game = GameService(self.state, self.render, self._focus_answer)

    def run(self):
        configure_page(self.page)
        self.page.add(top_bar(), self.content, footer())
        self.render()

    def _focus_answer(self):
        self.answer.focus()
        self.page.update()

    def _submit_from_field(self, _):
        self.game.submit_answer(self.answer.value)

    def render(self):
        if self.state.screen is Screen.LOBBY:
            view = LobbyScreen(self.game.start_match).build()
        elif self.state.screen is Screen.COUNTDOWN:
            view = CountdownScreen(self.state.countdown).build()
        else:
            view = GameScreen(self.state, self.answer, self.game.submit_answer, self.game.reset).build()
        self.content.content = ft.Container(content=view, alignment=ft.alignment.center, expand=True, padding=20)
        self.page.update()
