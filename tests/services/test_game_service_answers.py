"""Responsibility: GameService.choose_answer scores taps, deals new problems and ends the round."""

from unittest.mock import Mock

import pytest

from math_tug.services import game_service as game_service_module
from math_tug.config import WIN_LEAD
from math_tug.services.game_service import GameService
from math_tug.domain.player import Player
from math_tug.domain.state import Screen

LEFT, RIGHT = Player.LEFT, Player.RIGHT


@pytest.fixture
def service(state, rng):
    service = GameService(state, Mock(), rng)
    for player in Player:
        state.problems[player] = service._new_problem(None)
    state.screen = Screen.PLAYING
    return service


def right(state, player):
    problem = state.problems[player]
    return problem, problem.answer


def wrong(state, player):
    problem = state.problems[player]
    return problem, next(o for o in problem.options if o != problem.answer)


def tap(service, player, problem_and_choice):
    service.choose_answer(player, *problem_and_choice)


def test_right_answer_scores_one_point_for_that_player(service, state):
    tap(service, RIGHT, right(state, RIGHT))

    assert state.scores == {LEFT: 0, RIGHT: 1}


def test_wrong_answer_scores_nothing(service, state):
    tap(service, LEFT, wrong(state, LEFT))

    assert state.scores == {LEFT: 0, RIGHT: 0}


@pytest.mark.parametrize("answer", [right, wrong])
def test_answering_deals_a_new_problem_to_that_player_only(service, state, answer):
    before_left, before_right = state.problems[LEFT], state.problems[RIGHT]

    tap(service, LEFT, answer(state, LEFT))

    assert state.problems[LEFT].expression != before_left.expression
    assert state.problems[RIGHT] is before_right


def test_never_repeats_the_same_problem_twice_in_a_row(service, state, monkeypatch):
    current = state.problems[LEFT]
    fresh = game_service_module.make_problem(game_service_module.random.Random(0))
    assert fresh.expression != current.expression
    dealt = iter([current, current, fresh])
    monkeypatch.setattr(game_service_module, "make_problem", lambda rng, operations, tables: next(dealt))

    tap(service, LEFT, right(state, LEFT))

    assert state.problems[LEFT] is fresh


def test_records_the_attempt_for_feedback(service, state):
    problem, choice = wrong(state, RIGHT)

    tap(service, RIGHT, (problem, choice))

    attempt = state.last_attempts[RIGHT]
    assert (attempt.problem, attempt.choice, attempt.correct) == (problem, choice, False)
    assert state.last_attempts[LEFT] is None


def test_late_tap_on_an_old_problem_is_ignored(service, state):
    old = right(state, LEFT)
    tap(service, LEFT, old)

    tap(service, LEFT, old)  # e.g. a double tap arriving after the screen changed

    assert state.scores[LEFT] == 1


def test_tap_with_the_other_players_problem_is_ignored(service, state):
    tap(service, LEFT, right(state, RIGHT))

    assert state.scores == {LEFT: 0, RIGHT: 0}


def test_getting_far_enough_ahead_ends_the_round(service, state):
    for _ in range(WIN_LEAD):
        assert state.screen is Screen.PLAYING
        tap(service, RIGHT, right(state, RIGHT))

    assert state.screen is Screen.RESULT
    assert state.winner is RIGHT


def test_no_one_can_score_after_the_round_ends(service, state):
    for _ in range(WIN_LEAD):
        tap(service, LEFT, right(state, LEFT))

    tap(service, RIGHT, right(state, RIGHT))

    assert state.scores == {LEFT: WIN_LEAD, RIGHT: 0}
