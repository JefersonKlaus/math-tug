"""Responsibility: reading the phone's language (and falling back to English if it can't be read)."""

import asyncio
from types import SimpleNamespace

import flet as ft

from math_tug.ui.device_language import device_language, language_of
from tests.helpers import FakePage


def test_language_of_flet_locales():
    assert language_of([ft.Locale("pt", "BR")]) == "pt"
    assert language_of([ft.Locale("en", "US")]) == "en"
    assert language_of(None) == "en"


def test_portuguese_phone():
    assert asyncio.run(device_language(FakePage(languages=("pt",)))) == "pt"


def test_english_phone():
    assert asyncio.run(device_language(FakePage(languages=("en",)))) == "en"


def test_no_device_information_means_english():
    page = FakePage()

    async def no_info():
        return None

    page.get_device_info = no_info
    assert asyncio.run(device_language(page)) == "en"


def test_an_error_means_english():
    page = FakePage(languages=("pt",))

    async def broken():
        raise RuntimeError("not available on this platform")

    page.get_device_info = broken
    assert asyncio.run(device_language(page)) == "en"


def test_no_answer_means_english_instead_of_waiting_forever():
    page = FakePage(languages=("pt",))

    async def never_answers():
        await asyncio.Event().wait()
        return SimpleNamespace(locales=[ft.Locale("pt")])

    page.get_device_info = never_answers

    async def with_a_deadline():
        # If device_language had no time limit this would fail here instead of hanging the test run.
        return await asyncio.wait_for(device_language(page, timeout=0.01), 1)

    assert asyncio.run(with_a_deadline()) == "en"
