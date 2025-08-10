# Repository Guidelines

This document explains how to work on django-countries: where things live, how to run tests and checks, and what we expect in contributions.

## Project Structure & Modules
- Source: `django_countries/` (fields, filters, GraphQL, templates, static flags, locales).
- Tests: `django_countries/tests/` (pytest + pytest-django settings in `django_countries/tests/settings*.py`).
- Docs/Meta: `README.rst`, `CHANGES.rst`, `setup.cfg`, `tox.ini`, `.pre-commit-config.yaml`.

## Build, Test, and Dev Commands
- Install dev deps: `pip install -e .[dev]`.
- Prefer `uvx tox` to run the matrix (uses uv-managed, ephemeral tox).
- Quick local tests: `pytest` (DJANGO_SETTINGS_MODULE preconfigured).
- Type check: `uvx tox -e mypy` or `mypy django_countries`.
- Lint/format: `ruff check --fix .` and `ruff format .`.
- Security scan: `uvx tox -e bandit`.
- Readme/changes rendering: `uvx tox -e readme`.
- Coverage reports: `uvx tox -e coverage_report` (combines, enforces thresholds, outputs HTML).

## Coding Style & Naming
- Formatter/linter: Ruff (88 chars, Black-compatible). Run `pre-commit run -a`.
- Imports: managed by Ruff’s isort rules.
- Typing: mypy with `django-stubs`; prefer explicit types; avoid untyped calls.
- Tests: files named `test_*.py`; functions `test_*`; fixtures in `conftest.py`.

## Testing Guidelines
- Frameworks: `pytest`, `pytest-django`, `pytest-cov`.
- Coverage: aim ≥90% for package code; test files are expected to execute fully (strict run coverage enforced in tox).
- Keep tests fast and isolated; prefer public APIs; add regression tests for bugs.

## Commit & Pull Requests
- Commits: concise imperative subject (“Fix TypeError in CountryFilter”), reference issues (`Fixes #123`) when applicable.
- PRs must: describe motivation and behavior change, include tests, pass CI (`tox`) and type/lint checks, and update `CHANGES.rst` under the unreleased section.
- Screenshots only if UI assets change (e.g., flag updates).

## Security & Configuration Tips
- Never commit large binaries or generated assets; flags live under `django_countries/static/flags/`.
- Validate inputs touching serialization/filters; run `tox -e bandit`.

## Release Notes
- Add a short bullet to `CHANGES.rst` under the upcoming version; maintainers will handle versioning via zest.releaser.
