"""Responsibility: configure_page sets up a dark landscape app and locks phones to landscape."""

import flet as ft
import pytest

from math_tug.ui.page_setup import configure_page
from tests.helpers import FakePage


def test_dark_landscape_window(page):
    configure_page(page)

    assert page.title == "Math Tug"
    assert page.theme_mode == ft.ThemeMode.DARK
    assert (page.window.width, page.window.height) == (1200, 700)
    assert (page.window.min_width, page.window.min_height) == (568, 320)   # the smallest phone held sideways


@pytest.mark.parametrize("platform", [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS])
def test_phones_are_locked_to_landscape_either_way_round(platform):
    page = FakePage(platform=platform)

    configure_page(page)

    (handler, args), = page.tasks
    assert handler == page.set_allowed_device_orientations
    assert args == ([ft.DeviceOrientation.LANDSCAPE_LEFT, ft.DeviceOrientation.LANDSCAPE_RIGHT],)


@pytest.mark.parametrize("platform, web", [(ft.PagePlatform.WINDOWS, False), (ft.PagePlatform.MACOS, False), (ft.PagePlatform.ANDROID, True)])
def test_no_orientation_lock_on_desktop_or_web(platform, web):
    """Flet only supports the lock in the mobile app (it raises on desktop)."""
    page = FakePage(platform=platform, web=web)

    configure_page(page)

    assert page.tasks == []
