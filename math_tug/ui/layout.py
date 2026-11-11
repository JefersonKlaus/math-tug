"""The screen size the UI is built for."""

from dataclasses import dataclass

import flet as ft

MAX_CONTENT_WIDTH = 1100  # on big screens the game keeps its shape, centred
COMPACT_HEIGHT = 600      # below this page height (phones held sideways) everything gets tighter


@dataclass(frozen=True)
class Layout:
    """Screen size the UI is built for. The app is landscape: one layout, two size sets."""

    width: float
    height: float

    @classmethod
    def of(cls, page: ft.Page) -> "Layout":
        return cls(page.width or 1200, page.height or 700)

    @property
    def compact(self) -> bool:
        return self.height < COMPACT_HEIGHT

    @property
    def padding(self) -> int:
        return 8 if self.compact else 20

    @property
    def content_width(self) -> float:
        return min(self.width, MAX_CONTENT_WIDTH) - 2 * self.padding

    def pick(self, regular, compact):
        return compact if self.compact else regular
