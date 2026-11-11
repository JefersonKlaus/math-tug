import asyncio
import random

import pytest

from math_tug.ui.layout import Layout
from math_tug.domain.state import GameState
from tests.helpers import FakePage


@pytest.fixture
def page():
    return FakePage()


@pytest.fixture
def layout():
    """A typical phone held sideways."""
    return Layout(844, 390)


@pytest.fixture
def state():
    return GameState()


@pytest.fixture
def rng():
    return random.Random(1234)


@pytest.fixture
def no_sleep(monkeypatch):
    """Make ``asyncio.sleep`` return immediately and record the requested delays."""
    delays = []

    async def fake_sleep(seconds):
        delays.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    return delays


@pytest.fixture
def yielding_sleep(monkeypatch):
    """Make ``asyncio.sleep`` return almost at once but still let other tasks run.

    Lets a test do something (tap settings, restart...) while a countdown is waiting.
    Returns the real ``asyncio.sleep`` so the test can hand control to that countdown.
    """
    real_sleep = asyncio.sleep

    async def fake_sleep(seconds):
        await real_sleep(0)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    return real_sleep
