"""The app's languages: English (default) and Brazilian Portuguese, chosen from the phone's language."""

from .languages import DEFAULT_LANGUAGE, LANGUAGES, pick_language
from .translator import Translator

__all__ = ["DEFAULT_LANGUAGE", "LANGUAGES", "Translator", "pick_language"]
