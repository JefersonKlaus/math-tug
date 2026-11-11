"""Responsibility: app.py boots MathTugApp through Flet."""

import asyncio
import runpy
from pathlib import Path
from unittest.mock import Mock

import flet as ft

import app as entry
from tests.helpers import FakePage, app_parts, texts

APP_FILE = Path(__file__).resolve().parents[2] / "app.py"


def test_main_opens_the_app_in_the_phones_language():
    page = FakePage(languages=("pt",))

    asyncio.run(entry.main(page))

    assert "Prontos para " in texts(app_parts(page)[1])


def test_running_as_script_starts_flet_with_main(monkeypatch):
    fake_run = Mock()
    monkeypatch.setattr(ft, "run", fake_run)  # fails if Flet has no ft.run (needs Flet >= 1.0)

    namespace = runpy.run_path(str(APP_FILE), run_name="__main__")

    fake_run.assert_called_once_with(namespace["main"])


def test_importing_does_not_start_flet(monkeypatch):
    fake_run = Mock()
    monkeypatch.setattr(ft, "run", fake_run)

    runpy.run_path(str(APP_FILE), run_name="not_main")

    fake_run.assert_not_called()
