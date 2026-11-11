"""Which languages the app speaks, and which one to use for a phone."""

from collections.abc import Iterable

DEFAULT_LANGUAGE = "en"
LANGUAGES = ("en", "pt")


def pick_language(language_codes: Iterable[str]) -> str:
    """The first of the phone's languages (most preferred first) that the app speaks, else English.

    ``["pt"]`` (Brazil or Portugal) gives Portuguese, ``["en"]`` English, and a phone in
    another language falls back to English unless Portuguese is also in its list.
    """
    for code in language_codes:
        code = (code or "").lower()
        if code in LANGUAGES:
            return code
    return DEFAULT_LANGUAGE
