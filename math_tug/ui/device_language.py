"""Reading the phone's language."""

import asyncio
import logging

import flet as ft

from ..i18n import DEFAULT_LANGUAGE, pick_language

logger = logging.getLogger(__name__)


def language_of(locales) -> str:
    """The app language for a list of ``ft.Locale`` (most preferred first)."""
    return pick_language(locale.language_code for locale in locales or [])


async def device_language(page: ft.Page, timeout: float = 3) -> str:
    """The app language for the phone (or computer, or browser) the app runs on.

    If the device can't be asked, or takes too long to answer, the app starts in English.
    """
    try:
        info = await asyncio.wait_for(page.get_device_info(), timeout)
    except Exception:  # noqa: BLE001 - any failure just means "use the default"
        logger.warning("Could not read the device language; using %s", DEFAULT_LANGUAGE, exc_info=True)
        return DEFAULT_LANGUAGE
    return language_of(info.locales if info else [])
