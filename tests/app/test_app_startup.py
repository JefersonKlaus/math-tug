"""Responsibility: MathTugApp.run() assembles the page."""

from math_tug.app_controller import MathTugApp
from tests.helpers import app_parts, texts


def test_run_adds_header_lobby_and_footer(page):
    app = MathTugApp(page)
    app.run()

    header, content, footer = app_parts(page)
    assert header.content.controls[-1] is app.settings_button
    assert content is app.content and "Ready to " in texts(content)
    assert "v1.0.0" in texts(footer)
    assert page.title == "Math Tug"
