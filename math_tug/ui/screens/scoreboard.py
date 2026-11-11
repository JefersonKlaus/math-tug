"""Both sides, their scores and the rope (above the game and the result)."""

import flet as ft

from ...domain.player import Player
from ...domain.state import GameState
from ...i18n import Translator
from ...theme import PLAYER_COLORS
from ..components.avatar import avatar
from ..components.label import label
from ..components.tug_bar import tug_bar
from ..layout import Layout


def scoreboard(state: GameState, layout: Layout, tr: Translator):
    """One row: LEFT and its score, the rope, RIGHT and its score."""

    def side(player: Player):
        color = PLAYER_COLORS[player]
        parts = [
            avatar(tr(f"player.{player.value}.initial"), color, True),
            ft.Text(tr(f"player.{player.value}"), size=layout.pick(14, 12), weight=ft.FontWeight.BOLD),
            ft.Text(str(state.scores[player]), size=layout.pick(39, 28), color=color, weight=ft.FontWeight.BOLD),
        ]
        return ft.Row(parts if player is Player.LEFT else parts[::-1], spacing=8)

    # The rope gets what is left of the width next to both sides (at most 460 px).
    # A side is an avatar, the name and the score; names are longer in some languages.
    gap = layout.pick(18, 10)
    longest_name = max(len(tr(f"player.{player.value}")) for player in Player)
    side_width = 34 + 16 + longest_name * layout.pick(9, 7.5) + layout.pick(50, 36)
    rope_width = max(160, min(460, layout.content_width - 2 * (side_width + gap)))
    win_lead = state.settings.win_lead
    rope = ft.Column([tug_bar(state.lead, win_lead, rope_width), label(tr("scoreboard.rule", lead=win_lead), 9)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=layout.pick(4, 1), tight=True)
    return ft.Row([side(Player.LEFT), rope, side(Player.RIGHT)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=gap)
