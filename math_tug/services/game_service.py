"""The game flow."""

import asyncio
import random
from collections.abc import Callable

from ..domain.attempt import Attempt
from ..domain.player import Player
from ..domain.problem import Problem, make_problem
from ..domain.state import GameState, Screen

Render = Callable[[], None]


class GameService:
    """The game flow: countdown, answers, restart and going to and from settings."""

    def __init__(self, state: GameState, render: Render, rng: random.Random | None = None):
        self.state = state
        self.render = render
        self.rng = rng or random.Random()
        self._countdown = None  # identifies the countdown that is allowed to finish

    def _new_problem(self, previous: Problem | None) -> Problem:
        settings = self.state.settings
        problem = make_problem(self.rng, settings.operations, settings.tables)
        while previous is not None and problem.expression == previous.expression:
            problem = make_problem(self.rng, settings.operations, settings.tables)
        return problem

    async def start_match(self, _):
        if self.state.screen is not Screen.LOBBY:
            return  # ignore a second tap on START while the countdown runs
        await self._countdown_then_play()

    async def restart(self, _):
        """Start the game over: 0-0, new problems and a new 3-2-1 countdown."""
        if not self.state.match_in_progress:
            return
        self.state.reset()
        await self._countdown_then_play()

    async def _countdown_then_play(self):
        token = self._countdown = object()
        for player in Player:
            self.state.problems[player] = self._new_problem(None)
        self.state.screen = Screen.COUNTDOWN
        self.state.countdown = 3
        self.render()
        for value in (2, 1, None):
            await asyncio.sleep(0.7)
            if self._countdown is not token:
                return  # the game was ended or restarted while we waited
            if value is None:
                self.state.screen = Screen.PLAYING
            else:
                self.state.countdown = value
            self.render()

    def choose_answer(self, player: Player, problem: Problem, choice: int):
        if self.state.screen is not Screen.PLAYING:
            return  # the round is already over
        if self.state.problems[player] is not problem:
            return  # late tap on a problem that was already answered
        attempt = Attempt(problem, choice)
        self.state.last_attempts[player] = attempt
        if attempt.correct:
            self.state.scores[player] += 1
        if self.state.winner is not None:
            self.state.screen = Screen.RESULT
        else:
            self.state.problems[player] = self._new_problem(problem)
        self.render()

    def reset(self, _):
        self._countdown = None
        self.state.reset()
        self.render()

    def open_settings(self, _):
        """Go to the settings screen. Any game in progress is ended (the app asks first)."""
        self._countdown = None
        self.state.reset()
        self.state.screen = Screen.SETTINGS
        self.render()

    def close_settings(self, _):
        self.state.screen = Screen.LOBBY
        self.render()
