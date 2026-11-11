"""Responsibility: which language the app uses for a phone's languages."""

import pytest

from math_tug.i18n import DEFAULT_LANGUAGE, LANGUAGES, pick_language


def test_english_and_portuguese_english_first():
    assert LANGUAGES == ("en", "pt")
    assert DEFAULT_LANGUAGE == "en"


@pytest.mark.parametrize("phone, app", [
    (["pt"], "pt"),            # phone in Portuguese (Brazil or Portugal: only the language counts)
    (["en"], "en"),            # phone in English
    (["PT"], "pt"),            # case does not matter
    (["es", "pt"], "pt"),      # first language the app speaks
    (["pt", "en"], "pt"),
    (["en", "pt"], "en"),
    (["fr"], "en"),            # any other language: English
    ([], "en"),
    ([None], "en"),
])
def test_uses_the_first_phone_language_the_app_speaks_else_english(phone, app):
    assert pick_language(phone) == app
