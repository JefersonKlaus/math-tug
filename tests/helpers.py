"""Shared test utilities for inspecting Flet control trees without a running app."""

from types import SimpleNamespace

import flet as ft


class FakePage:
    """Minimal stand-in for ``ft.Page``.

    A real page needs a live Flet session. The app only sets a few attributes
    on the page and calls ``add`` and ``update``, so this records those calls.
    """

    def __init__(self, width=844, height=390, platform=ft.PagePlatform.ANDROID, web=False, languages=("en",)):
        self.window = SimpleNamespace()
        self.width, self.height = width, height  # a typical phone held sideways
        self.platform, self.web = platform, web
        self.languages = languages  # the phone's languages, most preferred first
        self.on_resize = None
        self.on_locale_change = None
        self.controls = []
        self.update_calls = 0
        self.dialogs = []  # like Flet, a closed dialog stays here until its closing animation ends
        self.tasks = []

    def run_task(self, handler, *args):
        self.tasks.append((handler, args))

    async def set_allowed_device_orientations(self, orientations):
        self.allowed_orientations = orientations

    async def get_device_info(self):
        return SimpleNamespace(locales=[ft.Locale(code) for code in self.languages])

    def add(self, *controls):
        self.controls.extend(controls)

    def update(self):
        self.update_calls += 1

    def show_dialog(self, dialog):
        # Same check as ft.Page.show_dialog. Deliberately stricter than Flet: real
        # Flet also wraps dialog.on_dismiss, which happens to make equal dialogs differ.
        if dialog in self.dialogs:
            raise RuntimeError("Dialog is already opened")
        dialog.open = True
        self.dialogs.append(dialog)

    def pop_dialog(self):
        dialog = next((d for d in reversed(self.dialogs) if d.open), None)
        if dialog is not None:
            dialog.open = False
        return dialog

    @property
    def open_dialog(self):
        return next((d for d in reversed(self.dialogs) if d.open), None)


def walk(control):
    """Yield ``control`` and every control nested beneath it, depth first."""
    if control is None:
        return
    yield control
    for child in getattr(control, "controls", None) or []:
        yield from walk(child)
    content = getattr(control, "content", None)
    if isinstance(content, ft.Control):
        yield from walk(content)


def texts(control):
    """Return the values of all ``ft.Text`` controls in the tree, in order."""
    return [c.value for c in walk(control) if isinstance(c, ft.Text)]


def find_all(control, control_type):
    return [c for c in walk(control) if isinstance(c, control_type)]


def find_key(control, key):
    matches = [c for c in walk(control) if c.key == key]
    assert len(matches) == 1, f"expected one control with key {key!r}, found {len(matches)}"
    return matches[0]


def buttons(control):
    return find_all(control, ft.Button)


def button_labels(control):
    return [b.content for b in buttons(control)]


def button_by_text(control, fragment):
    matches = [b for b in buttons(control) if fragment in b.content]
    assert len(matches) == 1, f"expected one button containing {fragment!r}, got {button_labels(control)}"
    return matches[0]


def app_parts(page):
    """The header, content and footer the app puts on the page (inside its SafeArea)."""
    (safe_area,) = page.controls
    assert isinstance(safe_area, ft.SafeArea)
    return safe_area.content.controls
