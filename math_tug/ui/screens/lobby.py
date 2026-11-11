"""The start screen: LEFT vs RIGHT and the Start button."""

import flet as ft

from ...domain.player import Player
from ...i18n import Translator
from ...theme import MUTED, PANEL, PINK, PLAYER_COLORS
from ..components.avatar import avatar
from ..components.label import label
from ..components.primary_button import primary_button
from ..layout import Layout
from .screen_column import screen_column


class LobbyScreen:
    def __init__(self, on_start, win_lead: int, layout: Layout, tr: Translator):
        self.on_start = on_start
        self.win_lead = win_lead
        self.layout = layout
        self.tr = tr

    def _player_card(self, player: Player):
        tr, color = self.tr, PLAYER_COLORS[player]
        return ft.Column(
            [avatar(tr(f"player.{player.value}.initial"), color, self.layout.compact), ft.Text(tr(f"player.{player.value}"), size=self.layout.pick(16, 13), weight=ft.FontWeight.BOLD, color=color)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=self.layout.pick(8, 2),
        )

    def build(self):
        layout, tr = self.layout, self.tr
        headline = layout.pick(58, 30)
        match_card = ft.Container(
            width=min(660, layout.content_width),
            padding=layout.pick(22, 8),
            bgcolor=PANEL,
            border=ft.Border.all(1, "#2B3A68"),
            border_radius=16,
            content=ft.Row(
                [
                    self._player_card(Player.LEFT),
                    ft.Row([ft.Container(width=34, height=1, bgcolor="#394A79"), ft.Text(tr("lobby.versus"), size=13, color=PINK, weight=ft.FontWeight.BOLD), ft.Container(width=34, height=1, bgcolor="#394A79")], spacing=10),
                    self._player_card(Player.RIGHT),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=layout.pick(70, 40),
            ),
        )
        return screen_column(
            [
                label(tr("lobby.kicker")),
                ft.Row([ft.Text(tr("lobby.headline"), size=headline, weight=ft.FontWeight.BOLD), ft.Text(tr("lobby.headline_accent"), size=headline, weight=ft.FontWeight.BOLD, color=PINK)], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(tr("lobby.tagline"), size=layout.pick(15, 12), color=MUTED, text_align=ft.TextAlign.CENTER),
                match_card,
                primary_button(tr("lobby.start"), self.on_start, layout.pick(48, 38)),
                ft.Text(tr("lobby.rule", lead=self.win_lead), size=layout.pick(11, 10), color="#7381A5"),
            ],
            layout, 10, 5, tight=True,
        )
