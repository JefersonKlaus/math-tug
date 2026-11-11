"""Responsibility: the Settings model (points ahead to win, operations and multiplication tables)."""

import pytest

from math_tug.domain.settings import Settings


@pytest.fixture
def settings():
    return Settings()


def test_defaults(settings):
    assert settings.win_lead == 3
    assert settings.operations == ("+", "-", "×", "÷")
    assert settings.tables == tuple(range(1, 11))


def test_set_win_lead(settings):
    settings.set_win_lead(7)
    assert settings.win_lead == 7


def test_rejects_a_win_lead_that_is_not_offered(settings):
    with pytest.raises(ValueError):
        settings.set_win_lead(4)
    assert settings.win_lead == 3


def test_toggle_an_operation_off_and_back_on_in_the_usual_order(settings):
    settings.toggle_operation("+")
    assert settings.operations == ("-", "×", "÷")
    settings.toggle_operation("+")
    assert settings.operations == ("+", "-", "×", "÷")


def test_last_operation_stays_on(settings):
    for op in ("+", "-", "×"):
        settings.toggle_operation(op)

    settings.toggle_operation("÷")

    assert settings.operations == ("÷",)


def test_toggle_a_table_off_and_back_on(settings):
    settings.toggle_table(7)
    assert 7 not in settings.tables
    settings.toggle_table(7)
    assert settings.tables == tuple(range(1, 11))


def test_last_table_stays_on(settings):
    for n in range(1, 10):
        settings.toggle_table(n)

    settings.toggle_table(10)

    assert settings.tables == (10,)


@pytest.mark.parametrize("toggle, value", [("toggle_operation", "^"), ("toggle_table", 11)])
def test_rejects_unknown_choices(settings, toggle, value):
    with pytest.raises(ValueError):
        getattr(settings, toggle)(value)


@pytest.mark.parametrize("off, uses", [(("×",), True), (("×", "÷"), False)])
def test_tables_only_matter_with_times_or_divide(settings, off, uses):
    for op in off:
        settings.toggle_operation(op)
    assert settings.uses_tables is uses

