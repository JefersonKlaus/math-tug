"""Responsibility: the Translator and the two sets of texts (English, Brazilian Portuguese)."""

import re

import pytest

from math_tug.i18n import Translator, en, pt


def placeholders(text):
    return set(re.findall(r"{(\w+)}", text))


def test_english_is_the_default():
    assert Translator().language == "en"


def test_both_languages_have_the_same_texts():
    assert set(en.STRINGS) == set(pt.STRINGS)


@pytest.mark.parametrize("key", sorted(en.STRINGS))
def test_translations_fill_in_the_same_values(key):
    assert placeholders(en.STRINGS[key]) == placeholders(pt.STRINGS[key])


def test_translator_fills_in_values():
    assert Translator("en")("lobby.rule", lead=5) == "Get 5 points ahead to win the round"
    assert Translator("pt")("lobby.rule", lead=5) == "Fique 5 pontos à frente para vencer a rodada"


def test_rejects_unknown_languages():
    with pytest.raises(ValueError):
        Translator("fr")
