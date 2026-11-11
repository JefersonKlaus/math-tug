"""What can be changed on the settings screen."""

from dataclasses import dataclass, field

from ..config import TABLE_CHOICES, WIN_LEAD, WIN_LEAD_CHOICES
from .problem import OPERATIONS


def _toggle(current: tuple, item, choices: tuple) -> tuple:
    """Switch ``item`` on or off, keeping ``choices`` order. The last item on stays on."""
    if item not in choices:
        raise ValueError(f"{item!r} is not one of {choices}")
    if item not in current:
        return tuple(c for c in choices if c in current or c == item)
    if len(current) > 1:
        return tuple(c for c in current if c != item)
    return current


@dataclass
class Settings:
    win_lead: int = WIN_LEAD
    operations: tuple[str, ...] = field(default=OPERATIONS)
    tables: tuple[int, ...] = field(default=TABLE_CHOICES)

    @property
    def uses_tables(self) -> bool:
        """Multiplication tables only matter when × or ÷ is on."""
        return "×" in self.operations or "÷" in self.operations

    def set_win_lead(self, value: int):
        if value not in WIN_LEAD_CHOICES:
            raise ValueError(f"win score must be one of {WIN_LEAD_CHOICES}, got {value}")
        self.win_lead = value

    def toggle_operation(self, operation: str):
        """Switch an operation on or off. The last operation left on cannot be switched off."""
        self.operations = _toggle(self.operations, operation, OPERATIONS)

    def toggle_table(self, table: int):
        """Switch a multiplication table on or off. The last table left on cannot be switched off."""
        self.tables = _toggle(self.tables, table, TABLE_CHOICES)
