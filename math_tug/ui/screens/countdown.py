"""The 3-2-1 before a game."""

import flet as ft

from ...i18n import Translator
from ...theme import MUTED, PINK
from ..components.label import label
from ..layout import Layout
from .screen_column import screen_column


class CountdownScreen:
    def __init__(self, countdown: int, layout: Layout, tr: Translator):
        self.countdown = countdown
        self.layout = layout
        self.tr = tr

    def build(self):
        layout, tr = self.layout, self.tr
        return screen_column(
            [
                label(tr("countdown.kicker")),
                ft.Text(str(self.countdown), size=layout.pick(150, 80), color=PINK, weight=ft.FontWeight.BOLD),
                ft.Text(tr("countdown.title"), size=layout.pick(23, 16), weight=ft.FontWeight.BOLD),
                ft.Text(tr("countdown.hint"), size=layout.pick(14, 12), color=MUTED),
            ],
            layout, 8, 2, tight=True,
        )
