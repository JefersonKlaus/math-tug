"""Responsibility: GameService.start_match deals problems, counts 3-2-1, starts play, and stops if the game is ended."""

import asyncio
from unittest.mock import Mock

import pytest

from math_tug.services.game_service import GameService
from math_tug.domain.state import Screen


@pytest.fixture
def snapshots():
    return []


@pytest.fixture
def service(state, rng, snapshots):
    render = Mock(side_effect=lambda: snapshots.append((state.screen, state.countdown)))
    return GameService(state, render, rng)


def test_counts_down_then_switches_to_playing(service, snapshots, no_sleep):
    asyncio.run(service.start_match(None))

    assert snapshots == [(Screen.COUNTDOWN, 3), (Screen.COUNTDOWN, 2), (Screen.COUNTDOWN, 1), (Screen.PLAYING, 1)]
    assert no_sleep == [0.7, 0.7, 0.7]


def test_problems_are_ready_before_the_countdown_shows(service, state, no_sleep):
    seen = []
    service.render = lambda: seen.append(all(state.problems.values()))

    asyncio.run(service.start_match(None))

    assert seen and all(seen)


def test_double_tap_on_start_runs_one_countdown(service, snapshots, no_sleep):
    async def double_tap():
        await asyncio.gather(service.start_match(None), service.start_match(None))

    asyncio.run(double_tap())

    assert snapshots.count((Screen.COUNTDOWN, 3)) == 1
    assert snapshots[-1][0] is Screen.PLAYING


def run_with_tap_during_countdown(service, state, tap, real_sleep):
    """Start a match, then call ``tap()`` while the countdown is waiting."""

    async def scenario():
        countdown = asyncio.create_task(service.start_match(None))
        await real_sleep(0)
        assert state.screen is Screen.COUNTDOWN
        tap()
        await countdown

    asyncio.run(scenario())


def test_ending_the_game_during_the_countdown_stops_it(service, state, snapshots, yielding_sleep):
    run_with_tap_during_countdown(service, state, lambda: service.open_settings(None), yielding_sleep)

    assert state.screen is Screen.SETTINGS  # the countdown did not jump back into the game
    assert (Screen.PLAYING, 1) not in snapshots


def test_reset_during_the_countdown_stops_it(service, state, yielding_sleep):
    run_with_tap_during_countdown(service, state, lambda: service.reset(None), yielding_sleep)

    assert state.screen is Screen.LOBBY


def test_old_countdown_cannot_hijack_a_new_match(service, state, snapshots, yielding_sleep):
    """End a game mid-countdown and start another: only the new countdown may run."""

    async def scenario():
        first = asyncio.create_task(service.start_match(None))
        await yielding_sleep(0)
        service.reset(None)
        second = asyncio.create_task(service.start_match(None))
        await asyncio.gather(first, second)

    asyncio.run(scenario())

    countdown_values = [c for screen, c in snapshots if screen is Screen.COUNTDOWN]
    assert countdown_values == [3, 3, 2, 1]  # first countdown showed 3 only, then the new one ran
    assert state.screen is Screen.PLAYING
