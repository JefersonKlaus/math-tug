# Task

A two-player math tug-of-war for phones, built entirely with Python and Flet. The app runs in **landscape** (phone held sideways) and adapts to the screen size, down to the smallest phones (568×320).

## Run locally

Requires Python 3.10 or newer.

```bash
python -m pip install -e .
flet run app.py
```

## How to play

Two players share one phone held sideways: **LEFT** (blue) and **RIGHT** (pink), side by side.

- After a 3-2-1 countdown, each side shows its own math problem with **3 answer buttons**. Only one is right.
- Each right answer is **1 point** and pulls the rope one step toward that player.
- A wrong answer scores nothing. The panel shows the right answer and the player gets a new problem.
- The game is **one round**, won by pulling the rope all the way: the first player to get **3 points ahead** of the other wins (the default, `WIN_LEAD` in `math_tug/config.py`, changeable in Settings). For example 3–0, 5–2 or 10–7 wins; 4–2 or 9–7 does not, so the game goes on.
- **RESTART GAME** (below the game, in the centre) starts the game over: 0–0, new problems and a new 3-2-1 countdown. Settings are kept.
- Problems are generated randomly from the chosen operations, with whole, non-negative numbers. × and ÷ come from the chosen multiplication tables (for example, the 7 table gives 7 × 8 and 56 ÷ 7). The + and − number ranges are in `math_tug/config.py`.

### Settings

The **SETTINGS** button (top right) opens the settings screen:

- **Points ahead to win:** 3 (default), 5, 7 or 10 (`WIN_LEAD_CHOICES` in `math_tug/config.py`).
- **Operations:** switch +, −, × and ÷ on or off. At least one always stays on.
- **Multiplication tables (for × and ÷):** choose which tables from 1 to 10 are used. Each table is multiplied by 1 to 10, and division divides by the table. At least one table always stays on. These buttons are dimmed when both × and ÷ are off.

The button can always be pressed. If a game is running (countdown or play), a popup asks first: **"End the game? Opening settings will finish the current game."** with **KEEP PLAYING** (the game goes on) and **END GAME** (the game ends and settings open). Settings are kept for as long as the app is open (they are not saved to disk).

## Languages

The app speaks **English** and **Brazilian Portuguese**, and it opens in the **phone's language** automatically (there is no language setting):

- A phone in Portuguese (Brazil or Portugal) gets Portuguese; a phone in English gets English.
- The app takes the first language in the phone's list of preferred languages that it speaks. A phone in any other language gets English, unless Portuguese is also in its list.
- The language is read before the first screen is drawn, so there is no flash of the wrong language. If the phone can't say (or doesn't answer within 3 seconds), the app opens in English.
- If the phone's language is changed while the app is open, the app follows it.
- On a computer or in a browser, the computer's or browser's language is used the same way.

Everything is translated, including the player names (LEFT/RIGHT → ESQUERDA/DIREITA), the header, the footer and the popup.

- The texts are in `math_tug/i18n/en.py` and `math_tug/i18n/pt.py`, under the same keys.
- `Translator` (`math_tug/i18n/translator.py`) looks a text up and fills in values: `tr("lobby.rule", lead=3)`.
- `pick_language` (`math_tug/i18n/languages.py`) chooses the language; `math_tug/ui/device_language.py` asks the phone.
- To add a language: copy `en.py`, translate the values, and add it to `LANGUAGES` (`languages.py`) and `_STRINGS` (`translator.py`). The tests check that every language has the same keys and placeholders, and that no screen shows English when Portuguese is on.

## Screen and orientation

- **Landscape only.** On phones and tablets the app locks itself to landscape, either way round, when it starts (`configure_page` in `math_tug/ui/page_setup.py`). Flet only supports this in the mobile app, so it is skipped on desktop and on the web. On Android 16 or later, devices 600 dp wide or more (large tablets) may ignore the lock.
- **On a computer** the window opens at 1200×700 and can be resized down to 568×320, the size of the smallest phone held sideways.
- **Adapts to the screen:** phones held sideways are short (about 320–430 px), so on screens shorter than 600 px (`COMPACT_HEIGHT`) the header, footer, text, buttons and spacing get smaller. Widths follow the screen (capped at 1100 px, centred). The game fills the screen; the other screens scroll if they still don't fit, so no button is ever hidden. The layout is rebuilt when the screen size changes.
- A `SafeArea` keeps the app clear of notches and the home indicator.

## Why `pyproject.toml` instead of `requirements.txt`

Project dependencies are declared in `pyproject.toml` (the `dependencies` list under `[project]`) rather than in a `requirements.txt` file, for these reasons:

- **It's the standard.** `pyproject.toml` is the official Python file for project configuration (PEP 518 / PEP 621). pip, uv, Poetry, PDM, Hatch and other tools all read it.
- **One file for everything.** The project name, version, supported Python version, dependencies and build settings all live together, so there's no separate `requirements.txt` to keep in sync.
- **Declares the Python version.** `requires-python = ">=3.10"` makes pip refuse to install on interpreters that can't run the code (the code uses the `X | None` syntax, which needs 3.10). `requirements.txt` can't express this.
- **Makes the project installable.** `pip install -e .` installs the dependencies and registers the `math_tug` package in the environment in editable mode, so code changes take effect without reinstalling.
- **Fits Flet's tooling.** Flet's own project templates use `pyproject.toml` and `flet build` reads it, so this file is ready for packaging the app later.

To add a dependency, add it to the `dependencies` list in `pyproject.toml` and run `python -m pip install -e .` again.

## Tests

```bash
python -m pip install -e ".[test]"
python -m pytest
```

`pytest` always measures coverage of `app.py` and `math_tug/` (including branches). The run fails if total coverage drops below **90%**. Settings are in `pyproject.toml` under `[tool.pytest.ini_options]` and `[tool.coverage.*]`. To run a single file without the coverage gate, add `--no-cov`:

```bash
python -m pytest tests/domain/test_state.py --no-cov
```

Each test file covers one responsibility, and the folders mirror `math_tug/`. The tests check behaviour (rules, what each screen shows, which buttons do what), not styling details such as sizes or colour codes:

| File | Responsibility |
| --- | --- |
| `domain/test_problem.py` | Generated problems: correct answers, 3 distinct options, no negatives, shuffled answer position, only chosen operations and tables |
| `domain/test_attempt.py` | An answer knows whether it was right |
| `domain/test_settings.py` | `Settings`: defaults (3 points ahead, all operations, tables 1–10), changing them, at least one operation and table stays on |
| `domain/test_state.py` | `GameState`: `lead`, `winner` (the player who is far enough ahead), `match_in_progress`, `reset` keeps settings and language |
| `services/test_game_service_countdown.py` | `start_match`: 3-2-1 countdown, double tap on Start, a countdown stops if the game is ended |
| `services/test_game_service_answers.py` | `choose_answer`: scoring, new problems, late or stale taps ignored, the round ends when someone is far enough ahead |
| `services/test_game_service_reset.py` | `reset` returns to the lobby |
| `services/test_game_service_restart.py` | `restart`: 0–0, new problems, new countdown, settings kept, only while a game is running |
| `services/test_game_service_navigation.py` | Going to settings (ends any game) and back to the lobby; new problems follow the settings |
| `services/test_settings_service.py` | Changing points ahead, operations and tables |
| `i18n/test_languages.py` | Which language a phone gets: Portuguese or English, first one the app speaks, otherwise English |
| `i18n/test_translator.py` | English is the default; both languages have the same texts and placeholders |
| `ui/test_layout.py` | `Layout`: screen size, compact sizes below 600 px high, content width capped on very wide screens |
| `ui/test_page_setup.py` | Dark theme, landscape window, landscape lock on phones (not on desktop or web) |
| `ui/test_device_language.py` | Reading the phone's language; English if it can't be read or takes too long |
| `ui/test_header.py` | Logo left, settings button right; slimmer on phones |
| `ui/test_footer.py` | Copyright, tagline and version; slimmer on phones |
| `ui/test_small_screens.py` | Every screen fits phones held sideways (568×320, 640×360) and tablets: nothing wider than the screen, compact sizes |
| `ui/test_translated_screens.py` | In Portuguese no screen (or the popup) still shows English |
| `ui/components/test_option_button.py` | An answer button shows its number |
| `ui/components/test_choice_button.py` | A settings choice: selected, dimmed when disabled, two digits fit |
| `ui/components/test_settings_button.py` | The Settings button |
| `ui/components/test_end_game_dialog.py` | The end-game popup: text, app design, actions, scrolls if needed |
| `ui/components/test_tug_bar.py` | Rope bar: the knot moves toward the leader and stops exactly at the winner's end |
| `ui/screens/test_lobby_screen.py` | Lobby: centred headline, LEFT vs RIGHT, win condition, Start button |
| `ui/screens/test_countdown_screen.py` | Countdown number and text |
| `ui/screens/test_scoreboard.py` | Sides, scores and rope; the rope leaves room for longer (Portuguese) names |
| `ui/screens/test_game_screen.py` | One panel per player (problem, 3 answers, feedback), Restart button below, only changed panels are rebuilt |
| `ui/screens/test_result_screen.py` | Winner announcement and Play Again button |
| `ui/screens/test_settings_screen.py` | Settings screen: the three sections (no language), current choices highlighted, taps reported, tables disabled without × and ÷ |
| `app/test_app_startup.py` | `MathTugApp.run()` builds header, lobby and footer |
| `app/test_app_rendering.py` | `render()` picks the right screen, screens scroll (the game fills the screen), rebuilds on resize, updates the game screen in place |
| `app/test_app_language.py` | The app opens in the phone's language and follows it when it changes |
| `app/test_settings_during_game.py` | Settings during a game: popup first, Keep playing / End game, double taps, asking again |
| `app/test_entry_point.py` | `app.py`: `main` opens the app in the phone's language; `__main__` start-up |
| `app/test_full_match.py` | Complete games through the on-screen buttons: win and play again, a close game, restart, settings, only the 7 table, on a Portuguese phone |

Shared helpers are in `tests/helpers.py` (a `FakePage` stand-in, so no Flet window is needed, plus functions to search the control tree). Shared fixtures are in `tests/conftest.py`.

## Structure

One file per responsibility or component:

```
app.py                          Flet entry point
math_tug/
  app_controller.py             builds the page and shows the right screen for the current state
  config.py                     game rules and problem number ranges
  theme.py                      colours (including each player's colour)
  i18n/                         languages.py (which language for a phone), translator.py, en.py, pt.py
  domain/                       the game itself, no UI
    player.py                   LEFT and RIGHT
    problem.py                  random multiple-choice problems
    attempt.py                  a player's answer to a problem
    settings.py                 points ahead, operations, tables
    state.py                    current screen, language and game state (scores, winner...)
  services/
    game_service.py             game flow: countdown, answers, restart, to and from settings
    settings_service.py         changing the settings
  ui/
    layout.py                   screen size and the two size sets (compact for phones)
    page_setup.py               window, theme, landscape lock
    device_language.py          reading the phone's language
    header.py, footer.py        the bars on every screen
    settings_opener.py          the Settings button: asks before ending a running game
    components/                 one widget per file: label, avatar, primary/secondary/settings/
                                restart/option/choice buttons, tug_bar, end_game_dialog
    screens/                    one screen per file: lobby, countdown, game, result, settings,
                                plus scoreboard and screen_column (shared layout)
tests/                          mirrors math_tug/ (see Tests)
docs/screenshots/               screenshots in both languages and on a small phone
pyproject.toml                  project metadata, dependencies, pytest and coverage settings
```
