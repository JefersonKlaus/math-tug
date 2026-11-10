import flet as ft

from .components import avatar, label, primary_button
from .config import BLUE, MUTED, PANEL, PINK
from .state import GameState


class LobbyScreen:
    def __init__(self, on_start):
        self.on_start = on_start

    def build(self):
        match_card = ft.Container(
            width=660,
            padding=22,
            bgcolor=PANEL,
            border=ft.border.all(1, "#2B3A68"),
            border_radius=16,
            content=ft.Row(
                [
                    ft.Column([avatar("JD", BLUE), ft.Text("Jamie Doe", weight=ft.FontWeight.BOLD), label("YOU", 9), ft.Text("⚡ 1,240", size=11, color="#A5B1D0")], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    ft.Row([ft.Container(width=34, height=1, bgcolor="#394A79"), ft.Text("VS", size=13, color=PINK, weight=ft.FontWeight.BOLD), ft.Container(width=34, height=1, bgcolor="#394A79")], spacing=10),
                    ft.Column([avatar("RX", PINK), ft.Text("Riley X", weight=ft.FontWeight.BOLD), label("READY", 9), ft.Text("⚡ 1,218", size=11, color="#A5B1D0")], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=70,
            ),
        )
        return ft.Column(
            [label("QUICK PLAY  •  1V1 ARENA"), ft.Row([ft.Text("Ready to ", size=58, weight=ft.FontWeight.BOLD), ft.Text("tug?", size=58, weight=ft.FontWeight.BOLD, color=PINK)], spacing=0), ft.Text("Solve faster. Pull harder. Be the last one standing.", size=15, color=MUTED), match_card, primary_button("START MATCH  →", self.on_start, 48), ft.Text("💡  First to solve 5 problems wins the round", size=10, color="#7381A5")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )


class CountdownScreen:
    def __init__(self, countdown: int):
        self.countdown = countdown

    def build(self):
        return ft.Column([label("GET READY"), ft.Text(str(self.countdown), size=150, color=PINK, weight=ft.FontWeight.BOLD), ft.Text("Eyes on the problem.", size=23, weight=ft.FontWeight.BOLD), ft.Text("The fastest answer pulls the rope.", color=MUTED)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)


class GameScreen:
    def __init__(self, state: GameState, answer: ft.TextField, on_submit, on_reset):
        self.state = state
        self.answer = answer
        self.on_submit = on_submit
        self.on_reset = on_reset

    def _scoreboard(self):
        rope_position = 38 + (self.state.player_score - self.state.opponent_score) * 5
        return ft.Row(
            [
                ft.Row([avatar("JD", BLUE, True), ft.Column([ft.Text("Jamie", size=13, weight=ft.FontWeight.BOLD), label("YOU", 8)])], spacing=8),
                ft.Text(str(self.state.player_score), size=39, color=BLUE, weight=ft.FontWeight.BOLD),
                ft.Stack([ft.Container(width=430, height=18, bgcolor="#263862", border_radius=12), ft.Container(left=215, top=-7, width=2, height=32, bgcolor="#FFCF69"), ft.Container(left=rope_position * 4.3, top=-7, width=32, height=30, bgcolor=PINK, border_radius=8, content=ft.Text("◆", size=9, color="white"), alignment=ft.alignment.center)], width=430, height=32),
                ft.Text(str(self.state.opponent_score), size=39, color=PINK, weight=ft.FontWeight.BOLD),
                ft.Row([ft.Column([ft.Text("Riley", size=13, weight=ft.FontWeight.BOLD), label("OPPONENT", 8)], horizontal_alignment=ft.CrossAxisAlignment.END), avatar("RX", PINK, True)], spacing=8),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=18,
        )

    def _body(self):
        if self.state.screen.value == "result":
            return ft.Container(margin=ft.margin.only(top=45), padding=30, bgcolor="#1B2A52", border=ft.border.all(1, "#3A4B7A"), border_radius=17, content=ft.Column([ft.Text("🏆", size=38), label("MATCH COMPLETE"), ft.Text("You pulled it off!", size=29, weight=ft.FontWeight.BOLD), ft.Text("Great speed, Jamie. Your new rating is 1,252.", size=13, color="#98A5C6"), primary_button("PLAY AGAIN  →", self.on_reset)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10))
        expression = self.state.current_problem[0]
        self.answer.value = ""
        return ft.Column([label("SOLVE TO PULL"), ft.Row([ft.Text(expression, size=52, weight=ft.FontWeight.BOLD), ft.Text("=", size=52, color="#7E8BAC"), self.answer], alignment=ft.MainAxisAlignment.CENTER), primary_button("SUBMIT ANSWER  ↵", lambda _: self.on_submit(self.answer.value), 45), ft.Text("━━━━━━  00:08", size=11, color="#7D8BAD")], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=18)

    def build(self):
        return ft.Column([ft.Row([ft.Column([label("ROUND 04  •  BEST OF 5"), ft.Text("Pull the rope!", size=27, weight=ft.FontWeight.BOLD)], spacing=7), ft.Text("🔥  3 STREAK", color="#FFC857", size=11)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=1050), self._scoreboard(), self._body()], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=28)
