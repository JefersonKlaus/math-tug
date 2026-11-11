"""The rope and its knot."""

import flet as ft

from ...theme import BLUE, GOLD, PINK

TUG_WIDTH = 460
KNOT_SIZE = 30


def knot_left(lead: int, win_lead: int, width: float = TUG_WIDTH) -> float:
    """x position of the rope knot; each point of lead pulls it one step to that side.

    The step is sized so that a lead of ``win_lead`` puts the knot at the end of the bar.
    """
    half = (width - KNOT_SIZE) / 2
    return half - lead * half / win_lead


def tug_bar(lead: int, win_lead: int, width: float = TUG_WIDTH):
    return ft.Stack(
        [
            ft.Container(left=0, top=11, width=width, height=12, bgcolor="#263862", border_radius=6),
            ft.Container(left=0, top=11, width=KNOT_SIZE, height=12, bgcolor=BLUE, border_radius=6),
            ft.Container(left=width - KNOT_SIZE, top=11, width=KNOT_SIZE, height=12, bgcolor=PINK, border_radius=6),
            ft.Container(left=width / 2 - 1, top=0, width=2, height=34, bgcolor=GOLD),
            ft.Container(
                left=knot_left(lead, win_lead, width),
                top=2,
                width=KNOT_SIZE,
                height=KNOT_SIZE,
                bgcolor="white",
                border=ft.Border.all(3, GOLD),
                border_radius=KNOT_SIZE,
            ),
        ],
        width=width,
        height=34,
    )
