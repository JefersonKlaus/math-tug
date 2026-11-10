import asyncio
from collections.abc import Callable

from .state import GameState, Screen


Render = Callable[[], None]
Focus = Callable[[], None]


class GameService:
    def __init__(self, state: GameState, render: Render, focus_answer: Focus):
        self.state = state
        self.render = render
        self.focus_answer = focus_answer

    async def start_match(self, _):
        self.state.screen = Screen.COUNTDOWN
        self.state.countdown = 3
        self.render()
        for value in (2, 1):
            await asyncio.sleep(0.7)
            self.state.countdown = value
            self.render()
        await asyncio.sleep(0.7)
        self.state.screen = Screen.PLAYING
        self.render()
        self.focus_answer()

    def submit_answer(self, answer: str):
        if not answer.strip():
            return
        if answer.strip() == self.state.current_problem[1]:
            self.state.player_score += 1
        if self.state.is_last_problem:
            self.state.screen = Screen.RESULT
        else:
            self.state.problem_index += 1
        self.render()

    def reset(self, _):
        self.state.reset()
        self.render()
