"""The game: one panel per player, the Restart button below."""

import flet as ft

from ...domain.player import Player
from ...domain.state import GameState
from ...i18n import Translator
from ...theme import GREEN, PANEL, PLAYER_COLORS, RED
from ..components.label import label
from ..components.option_button import option_button
from ..components.restart_button import restart_button
from ..layout import Layout
from .scoreboard import scoreboard
from .screen_column import screen_column


class GameScreen:
    """The playing screen. It is built once per match and then refreshed in place.

    Only a panel whose problem or feedback changed is rebuilt, so the other
    player's buttons keep their identity and a tap already on its way from
    that player is not lost.
    """

    def __init__(self, state: GameState, on_choose, on_restart, layout: Layout, tr: Translator):
        self.state = state
        self.on_choose = on_choose
        self.on_restart = on_restart
        self.layout = layout
        self.tr = tr
        self._scoreboard = ft.Container()
        self._panels = {player: self._panel(player) for player in Player}
        self._shown = {}

    def _feedback(self, player: Player):
        size = self.layout.pick(15, 12)
        attempt = self.state.last_attempts[player]
        if attempt is None:
            return ft.Text("", size=size)
        if attempt.correct:
            icon, color, text = ft.Icons.CHECK_CIRCLE, GREEN, self.tr("game.correct")
        else:
            icon, color, text = ft.Icons.CANCEL, RED, self.tr("game.wrong", expression=attempt.problem.expression, answer=attempt.problem.answer)
        return ft.Row([ft.Icon(icon, color=color, size=size + 3), ft.Text(text, size=size, color=color, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

    def _panel(self, player: Player):
        return ft.Container(
            key=f"panel-{player.value}",
            expand=True,
            padding=ft.Padding.symmetric(horizontal=self.layout.pick(20, 8), vertical=self.layout.pick(8, 4)),
            bgcolor=PANEL,
            border=ft.Border.all(2, PLAYER_COLORS[player]),
            border_radius=self.layout.pick(22, 14),
            alignment=ft.Alignment.CENTER,
        )

    def _panel_content(self, player: Player):
        layout, tr = self.layout, self.tr
        color = PLAYER_COLORS[player]
        problem = self.state.problems[player]
        options = [
            option_button(value, color, lambda _, value=value: self.on_choose(player, problem, value), layout.pick(56, 40), layout.pick(28, 20))
            for value in problem.options
        ]
        return ft.Column(
            [
                label(tr("game.tap", player=tr(f"player.{player.value}")), layout.pick(10, 9), color),
                ft.Text(problem.expression, size=layout.pick(44, 24), weight=ft.FontWeight.BOLD),
                ft.Row(options, spacing=layout.pick(12, 8)),
                ft.Container(content=self._feedback(player), height=layout.pick(22, 16)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=layout.pick(10, 4),
            tight=True,
        )

    def refresh(self):
        self._scoreboard.content = scoreboard(self.state, self.layout, self.tr)
        for player in Player:
            shown = (self.state.problems[player], self.state.last_attempts[player])
            if self._shown.get(player) != shown:
                self._panels[player].content = self._panel_content(player)
                self._shown[player] = shown

    def build(self):
        self.refresh()
        # The panels grow to fill the height left between the scoreboard and the Restart button.
        return screen_column(
            [
                self._scoreboard,
                ft.Row([self._panels[Player.LEFT], self._panels[Player.RIGHT]], spacing=self.layout.pick(24, 10), expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH),
                restart_button(self.tr("game.restart"), self.on_restart, self.layout.pick(36, 30)),
            ],
            self.layout, 10, 5, expand=True,
        )
