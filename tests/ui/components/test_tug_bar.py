"""Responsibility: the rope bar and where its knot sits for a given lead and points ahead to win."""

import random

import pytest

from math_tug.ui.components.tug_bar import KNOT_SIZE, TUG_WIDTH, knot_left, tug_bar
from math_tug.config import WIN_LEAD_CHOICES
from math_tug.domain.player import Player
from math_tug.domain.state import GameState


def test_knot_starts_in_the_centre():
    assert knot_left(0, 3) == pytest.approx((TUG_WIDTH - KNOT_SIZE) / 2)


def test_knot_moves_towards_the_player_who_leads():
    assert knot_left(1, 3) < knot_left(0, 3) < knot_left(-1, 3)


@pytest.mark.parametrize("win_lead", WIN_LEAD_CHOICES)
def test_knot_stays_on_the_bar_and_ends_at_the_winners_side(win_lead):
    for seed in range(50):
        rng = random.Random(seed)
        state = GameState()
        state.settings.set_win_lead(win_lead)
        while state.winner is None:
            state.scores[rng.choice(list(Player))] += 1
            assert 0 <= knot_left(state.lead, win_lead) <= TUG_WIDTH - KNOT_SIZE

        end = 0 if state.winner is Player.LEFT else TUG_WIDTH - KNOT_SIZE
        assert knot_left(state.lead, win_lead) == pytest.approx(end)


def test_bar_draws_the_knot_where_it_belongs():
    assert tug_bar(-2, 5).controls[-1].left == pytest.approx(knot_left(-2, 5))
