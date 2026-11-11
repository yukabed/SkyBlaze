# Contributing

## Setup

No dependencies are required. A virtual environment is optional:

```bash
python -m venv .venv
python -m pip install -e .
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Ground rules

- Keep behaviour changes separate from refactors: one commit per behaviour fix,
  with a test that shows the before and after.
- Constants and asset paths belong in `config.py`, not inline.
- Entities hold their own behaviour; shared state belongs in `Game`.
- Never name a method or attribute on a `turtle.Turtle` subclass after an
  existing `Turtle` method (`speed`, `shape`, `clear`, `write`, ...); it would
  silently replace it.
- Do not commit `.env` files or secrets (there are none today).
