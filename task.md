T 2:17

### Challenge description

The first goal is to transform the current mock game (screens) into a functional mobile app. It means, thhe implementation must preserv the visual concept while making the game flow workd end to end. After this furst implementation, it will be tested to find visual improvementes (UX).
The second goal is adding unit test and create a build to be installed at my mobile app.
The last goal, is make the app run in two languages, portugues and english, the default language will be english, but, it the cellphone is in portugueses it will use the portugues language.

## How to judge completion
Run the application and play an entire match with my daughter, confirming that the UI is working well and we do not have BUGs. After the game, run the pytests and all new tests need to pass.
Today the game is mocked, so, we only have screens, to be considered DONE, this app needs to work in a mobile device.

## Notes
This is a tug of war game designet to help children improve their mathematics skills. This is a two player game, where they need to share the same device, and play one againt the other, solving mathematics problems.
This is a open source project and you can find it here https://github.com/JefersonKlaus/math-tug.

## Evidence
The evidence must include:

- Running the game and completing an entire match in hard mode.
- Playing through selection confirmation, math challenges, timers, and the best-of-5 rule.
- Opening the settings screen and confirming that the available game options can be selected.
- Running the complete automated test suite after the manual playthrough.

SETUP:

```bash
cd workspace/calculo-da-velha
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

ACTION: `flet run`

RESULT: The game opened and an entire hard-mode match was played successfully.

ACTION: `pytest`

RESULT: The complete test suite passed.








## Evidence
I ran the game and could play it with my daugthers, and if you open the settig screen you can choose the number, and levels. And after the game I ran the unit tests.

SETUP:
cd workspace/math-tug
source .venv/bin/activate
python -m pip install -e .


ACTION: flet run app.py
RESULT: The game opened and I played it

ACTION: pytest
RESULT: 236 passed in 1.45s


## #########################