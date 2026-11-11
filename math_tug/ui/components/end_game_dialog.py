"""The popup that asks before settings end a running game."""

import flet as ft

from ...theme import PINK
from .label import label
from .primary_button import primary_button
from .secondary_button import secondary_button


def end_game_dialog(tr, on_keep_playing, on_end_game):
    """Asks before settings end a running game. Styled like the result card."""
    return ft.AlertDialog(
        modal=True,
        bgcolor="#1B2A52",
        barrier_color="#CC0B1122",
        shape=ft.RoundedRectangleBorder(radius=20, side=ft.BorderSide(2, PINK)),
        icon=ft.Icon(ft.Icons.SETTINGS, color=PINK, size=32),
        title=ft.Column([label(tr("dialog.kicker")), ft.Text(tr("dialog.title"), size=24, weight=ft.FontWeight.BOLD)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, tight=True),
        # Tight paddings and scrolling so it fits a phone held sideways (about 300 px high).
        inset_padding=ft.Padding.symmetric(horizontal=20, vertical=8),
        icon_padding=ft.Padding.only(top=16),
        title_padding=ft.Padding.only(left=24, right=24, top=8),
        content_padding=ft.Padding.only(left=24, right=24, top=12, bottom=18),
        scrollable=True,
        # The buttons live in the body (not `actions`, which Flutter aligns to the right) so they stay centred.
        content=ft.Column(
            [
                ft.Text(tr("dialog.message"), size=14, color="#98A5C6", text_align=ft.TextAlign.CENTER),
                ft.Row(
                    [secondary_button(tr("dialog.keep_playing"), on_keep_playing, height=42), primary_button(tr("dialog.end_game"), on_end_game, 42)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            tight=True,
        ),
    )
