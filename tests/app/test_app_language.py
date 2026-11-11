"""Responsibility: the app opens in the phone's language and follows it if it changes."""

import asyncio
from types import SimpleNamespace

import flet as ft
import pytest

from math_tug.app_controller import MathTugApp
from math_tug.domain.state import Screen
from tests.helpers import FakePage, app_parts, texts


def started(languages):
    page = FakePage(languages=languages)
    app = MathTugApp(page)
    asyncio.run(app.start())
    return app, page


@pytest.mark.parametrize("languages, headline, button", [
    (("pt",), "Prontos para ", "CONFIGURAÇÕES"),
    (("en",), "Ready to ", "SETTINGS"),
    (("fr",), "Ready to ", "SETTINGS"),
])
def test_opens_in_the_phones_language(languages, headline, button):
    app, page = started(languages)

    assert headline in texts(app.content)
    assert app.settings_button.content == button
    assert page.update_calls == 1   # drawn once, already in the right language


def test_follows_the_phone_when_its_language_changes():
    app, page = started(("pt",))

    page.on_locale_change(SimpleNamespace(locales=[ft.Locale("en", "US")]))

    assert "Ready to " in texts(app.content)
    assert app.settings_button.content == "SETTINGS"
    assert "NO CALCULATORS. JUST BRAINS." in texts(app_parts(page)[2])


def test_a_language_change_during_a_game_redraws_the_game(no_sleep):
    app, page = started(("en",))
    asyncio.run(app.game.start_match(None))
    assert app.state.screen is Screen.PLAYING

    page.on_locale_change(SimpleNamespace(locales=[ft.Locale("pt", "BR")]))

    assert "ESQUERDA  •  TOQUE NA RESPOSTA" in texts(app.content)


def test_the_same_language_again_changes_nothing():
    app, page = started(("en",))
    updates = page.update_calls

    page.on_locale_change(SimpleNamespace(locales=[ft.Locale("en", "GB")]))

    assert page.update_calls == updates
