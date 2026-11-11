"""The app: builds the page and shows the right screen for the current state."""

import flet as ft

from .domain.state import GameState, Screen
from .i18n import Translator
from .services.game_service import GameService
from .services.settings_service import SettingsService
from .ui.components.label import label
from .ui.components.settings_button import settings_button
from .ui.device_language import device_language, language_of
from .ui.footer import fit_footer, footer
from .ui.header import fit_header, header
from .ui.layout import Layout
from .ui.page_setup import configure_page
from .ui.screens.countdown import CountdownScreen
from .ui.screens.game import GameScreen
from .ui.screens.lobby import LobbyScreen
from .ui.screens.result import ResultScreen
from .ui.screens.settings import SettingsScreen
from .ui.settings_opener import SettingsOpener


class MathTugApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = GameState()
        self.content = ft.Container(expand=True)
        self.game = GameService(self.state, self.render)
        self.settings = SettingsService(self.state, self.render)
        self.settings_opener = SettingsOpener(page, self.state, self.game, lambda: self.tr)
        self.settings_button = settings_button("", self.settings_opener.on_click)
        self.footer_tagline = label("", 9)
        self.header = header(self.settings_button)
        self.footer = footer(self.footer_tagline)
        self._game_screen: GameScreen | None = None

    async def start(self):
        """Open in the phone's language (English or Portuguese), then show the app."""
        self.state.language = await device_language(self.page)
        self.run()

    def run(self):
        configure_page(self.page)
        self.page.on_resize = self._on_resize
        self.page.on_locale_change = self._on_locale_change
        # SafeArea keeps the app clear of notches and the home indicator.
        self.page.add(ft.SafeArea(content=ft.Column([self.header, self.content, self.footer], spacing=0, expand=True), expand=True))
        self.render()

    @property
    def tr(self) -> Translator:
        return Translator(self.state.language)

    def _view(self, layout: Layout, tr: Translator):
        game, settings = self.game, self.settings
        if self.state.screen is Screen.LOBBY:
            return LobbyScreen(game.start_match, self.state.settings.win_lead, layout, tr).build()
        if self.state.screen is Screen.SETTINGS:
            return SettingsScreen(self.state.settings, settings.set_win_lead, settings.toggle_operation, settings.toggle_table, game.close_settings, layout, tr).build()
        if self.state.screen is Screen.COUNTDOWN:
            return CountdownScreen(self.state.countdown, layout, tr).build()
        if self.state.screen is Screen.PLAYING:
            self._game_screen = GameScreen(self.state, game.choose_answer, game.restart, layout, tr)
            return self._game_screen.build()
        return ResultScreen(self.state, game.reset, layout, tr).build()

    def _on_resize(self, _):
        self._game_screen = None  # the screen size changed: rebuild for the new size
        self.render()

    def _on_locale_change(self, e):
        """The phone's language was changed while the app is open: follow it."""
        language = language_of(e.locales)
        if language != self.state.language:
            self.state.language = language
            self._game_screen = None  # rebuild every text in the new language
            self.render()

    def render(self):
        if self.state.screen is Screen.PLAYING and self._game_screen is not None:
            # Update the playing screen in place; rebuilding it would drop the
            # other player's in-flight tap (see GameScreen).
            self._game_screen.refresh()
        else:
            self._game_screen = None
            layout, tr = Layout.of(self.page), self.tr
            fit_header(self.header, layout)
            fit_footer(self.footer, layout)
            self.settings_button.content = tr("header.settings")
            self.footer_tagline.value = tr("footer.tagline")
            view = self._view(layout, tr)
            if self.state.screen is Screen.PLAYING:
                # The game fills the screen: its panels stretch to the height that is left.
                self.content.content = ft.Container(content=view, padding=layout.padding, expand=True)
            else:
                # Scrolls only if a screen is taller than the phone, so no button is ever out of reach.
                # (Inside a scroll view a Column only centres vertically; the Row centres horizontally.)
                self.content.content = ft.Column(
                    [ft.Row([ft.Container(content=view, padding=layout.padding)], alignment=ft.MainAxisAlignment.CENTER)],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                )
        self.page.update()
