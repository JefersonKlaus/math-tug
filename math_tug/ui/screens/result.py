"""Who won, and Play again."""

import flet as ft

from ...domain.player import Player
from ...domain.state import GameState
from ...i18n import Translator
from ...theme import PLAYER_COLORS
from ..components.label import label
from ..components.primary_button import primary_button
from ..layout import Layout
from .scoreboard import scoreboard
from .screen_column import screen_column


class ResultScreen:
    def __init__(self, state: GameState, on_reset, layout: Layout, tr: Translator):
        self.state = state
        self.on_reset = on_reset
        self.layout = layout
        self.tr = tr

    def build(self):
        layout, tr = self.layout, self.tr
        winner = self.state.winner
        color = PLAYER_COLORS[winner]
        left, right = self.state.scores[Player.LEFT], self.state.scores[Player.RIGHT]
        card = ft.Container(
            width=min(520, layout.content_width),
            padding=ft.Padding.symmetric(horizontal=layout.pick(30, 16), vertical=layout.pick(20, 8)),
            bgcolor="#1B2A52",
            border=ft.Border.all(2, color),
            border_radius=20,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.EMOJI_EVENTS, color=color, size=layout.pick(44, 28)),
                    label(tr("result.kicker")),
                    ft.Text(tr("result.winner", player=tr(f"player.{winner.value}")), size=layout.pick(34, 22), weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(tr("result.score", left=left, right=right), size=layout.pick(15, 12), color="#98A5C6"),
                    primary_button(tr("result.play_again"), self.on_reset, layout.pick(46, 34)),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=layout.pick(8, 3),
                tight=True,
            ),
        )
        return screen_column([scoreboard(self.state, layout, tr), card], layout, 18, 6, tight=True)
