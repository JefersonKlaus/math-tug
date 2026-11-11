"""Responsibility: GameService.restart starts the game over (0-0, new problems, new countdown)."""

import asyncio
from unittest.mock import Mock

import pytest

from math_tug.services.game_service import GameService
from math_tug.domain.player import Player
from math_tug.domain.state import Screen

LEFT, RIGHT = Player.LEFT, Player.RIGHT


@pytest.fixture
def snapshots():
    return []


@pytest.fixture
def service(state, rng, snapshots):
    render = Mock(side_effect=lambda: snapshots.append((state.screen, state.countdown)))
    return GameService(state, render, rng)


@pytest.fixture
def mid_game(service, state, no_sleep, snapshots):
    asyncio.run(service.start_match(None))
    problem = state.problems[LEFT]
    service.choose_answer(LEFT, problem, problem.answer)
    problem = state.problems[RIGHT]
    service.choose_answer(RIGHT, problem, next(o for o in problem.options if o != problem.answer))
    snapshots.clear()
    return state


def test_restart_clears_the_score_and_deals_new_problems(service, mid_game):
    before = dict(mid_game.problems)

    asyncio.run(service.restart(None))

    assert mid_game.scores == {LEFT: 0, RIGHT: 0}
    assert mid_game.last_attempts == {LEFT: None, RIGHT: None}
    assert all(mid_game.problems[p] is not before[p] for p in Player)


def test_restart_runs_the_countdown_again_then_plays(service, mid_game, snapshots):
    asyncio.run(service.restart(None))

    assert snapshots == [(Screen.COUNTDOWN, 3), (Screen.COUNTDOWN, 2), (Screen.COUNTDOWN, 1), (Screen.PLAYING, 1)]


def test_restart_keeps_the_settings(service, mid_game):
    mid_game.settings.set_win_lead(7)

    asyncio.run(service.restart(None))

    assert mid_game.settings.win_lead == 7


def test_taps_on_problems_from_before_the_restart_are_ignored(service, mid_game):
    old = mid_game.problems[LEFT]
    asyncio.run(service.restart(None))

    service.choose_answer(LEFT, old, old.answer)

    assert mid_game.scores[LEFT] == 0


def test_ignored_when_no_game_is_running(service, state, snapshots, no_sleep):
    state.screen = Screen.RESULT
    state.scores[LEFT] = 3

    asyncio.run(service.restart(None))

    assert state.screen is Screen.RESULT
    assert state.scores[LEFT] == 3
    assert snapshots == []


def test_restart_during_the_countdown_starts_it_again(service, state, snapshots, yielding_sleep):
    async def scenario():
        first = asyncio.create_task(service.start_match(None))
        await yielding_sleep(0)
        await asyncio.gather(first, service.restart(None))

    asyncio.run(scenario())

    countdown_values = [c for screen, c in snapshots if screen is Screen.COUNTDOWN]
    restarted_at = len(countdown_values) - 1 - countdown_values[::-1].index(3)
    assert countdown_values.count(3) == 2                  # the countdown started again
    assert countdown_values[restarted_at:] == [3, 2, 1]     # and the old one showed nothing after that
    assert [s for s, _ in snapshots].count(Screen.PLAYING) == 1
