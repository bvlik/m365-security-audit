# Contributing

Thanks for your interest! This project favours small, focused, read-only checks.

## Dev setup
```bash
pip install -r requirements.txt
pip install ruff bandit pytest
```

## Before opening a PR
- `ruff check .` — lint
- `bandit -r .` — security scan
- `python -m compileall .` — syntax
- `pytest -q` — tests (where present)

## Adding a check / rule
Drop one file in the `checks/` (or `rules/`) package, subclass the base class, and add it to the
registry. Keep it **read-only** and give every finding a clear title, severity and remediation.

## Conventions
- Conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`, `test:`)
- Type hints, small functions, no secrets in code
