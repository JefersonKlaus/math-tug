# Math Tug

A landscape-first mobile game mockup built entirely with Python and Flet.

## Run locally

```bash
python -m pip install -r requirements.txt
flet run app.py
```

The prototype includes:

- English-only lobby and match screens
- Mock 1v1 player matchup
- Countdown before the round
- Math problem answer flow
- Rope position and score feedback
- Match result and replay action

## Structure

- `app.py`: Flet entry point
- `math_tug/app_controller.py`: application orchestration and rendering
- `math_tug/game_service.py`: game transitions and answer rules
- `math_tug/state.py`: game state and domain queries
- `math_tug/screens.py`: screen composition
- `math_tug/components.py`: reusable Flet controls
- `math_tug/layout.py`: page setup and shared layout
- `math_tug/config.py`: colors and problem data