"""Looking texts up in the current language."""

from . import en, pt
from .languages import DEFAULT_LANGUAGE

_STRINGS = {"en": en.STRINGS, "pt": pt.STRINGS}


class Translator:
    """Looks up a text by key in one language: ``tr("lobby.rule", lead=3)``."""

    def __init__(self, language: str = DEFAULT_LANGUAGE):
        if language not in _STRINGS:
            raise ValueError(f"unknown language {language!r}")
        self.language = language
        self._strings = _STRINGS[language]

    def __call__(self, key: str, **values) -> str:
        return self._strings[key].format(**values)
