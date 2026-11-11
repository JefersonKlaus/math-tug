"""Points ahead to win, operations and multiplication tables."""

import flet as ft

from ...config import TABLE_CHOICES, WIN_LEAD_CHOICES
from ...domain.problem import OPERATIONS
from ...domain.settings import Settings
from ...i18n import Translator
from ..components.choice_button import choice_button
from ..components.label import label
from ..components.primary_button import primary_button
from ..layout import Layout
from .screen_column import screen_column


class SettingsScreen:
    def __init__(self, settings: Settings, on_win_lead, on_toggle_operation, on_toggle_table, on_done, layout: Layout, tr: Translator):
        self.settings = settings
        self.on_win_lead = on_win_lead
        self.on_toggle_operation = on_toggle_operation
        self.on_toggle_table = on_toggle_table
        self.on_done = on_done
        self.layout = layout
        self.tr = tr

    def _section(self, key: str, title: str, choices, spacing: int):
        row = ft.Row(choices, alignment=ft.MainAxisAlignment.CENTER, spacing=spacing, run_spacing=spacing, wrap=True, tight=True)
        return ft.Column([label(title), row], key=key, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=self.layout.pick(8, 2), tight=True)

    def build(self):
        settings, layout, tr = self.settings, self.layout, self.tr
        height, width = layout.pick(52, 36), layout.pick(64, 52)
        points = [choice_button(str(value), value == settings.win_lead, lambda _, value=value: self.on_win_lead(value), width, height=height) for value in WIN_LEAD_CHOICES]
        operations = [choice_button(op, op in settings.operations, lambda _, op=op: self.on_toggle_operation(op), width, height=height) for op in OPERATIONS]
        tables = [choice_button(str(n), n in settings.tables, lambda _, n=n: self.on_toggle_table(n), layout.pick(54, 46), settings.uses_tables, height) for n in TABLE_CHOICES]
        return screen_column(
            [
                ft.Text(tr("settings.title"), size=layout.pick(30, 18), weight=ft.FontWeight.BOLD),
                ft.Row([self._section("points", tr("settings.points"), points, 10), self._section("operations", tr("settings.operations"), operations, 10)], alignment=ft.MainAxisAlignment.CENTER, spacing=layout.pick(40, 20), wrap=True, tight=True),
                self._section("tables", tr("settings.tables"), tables, layout.pick(8, 6)),
                primary_button(tr("settings.done"), self.on_done, layout.pick(44, 34)),
            ],
            layout, 14, 5, tight=True,
        )
