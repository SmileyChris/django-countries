================
Developer Guide
================

This project targets Python 3.9+ (keeps 3.7-safe code paths) and Django 4.2/5.x. Use uv + tox for fast, reproducible workflows.

Quick Start
-----------
- Install tools: ``pipx install uv`` (or use a venv), Git, optional GPG (for signed tags).
- Run matrix: ``uvx tox``. Single env: ``uvx tox -e py313-django52``.

Test & Lint
-----------
- Tests: ``uvx tox -e py39-django42`` or ``uvx tox -e py313-django52``.
- Coverage: ``uvx tox -e coverage_report`` (enforces 100% tests, ≥90% package; outputs ``htmlcov/``).
  True coverage requires running all tests.
- Lint/format: ``uvx ruff check --fix .`` and ``uvx ruff format .``.
- Types: ``uvx tox -e mypy`` (mypy + django-stubs).
- Security: ``uvx tox -e bandit``.

Change Log (Towncrier)
----------------------
- Add a fragment under ``changes/`` per PR, e.g. ``123.feature.rst``, ``456.bugfix.rst``, ``789.misc.rst``.
  For fragments not directly related to a PR, use ``+anything.feature.rst``.
- Categories: breaking, feature, bugfix, doc, misc. Reference issues like ``(#123)`` in the fragment.
- Release notes are generated at the ``.. towncrier release notes start`` marker in ``CHANGES.rst``.

Release Process (maintainers)
-----------------------------
Scripted (recommended)
^^^^^^^^^^^^^^^^^^^^^^
- Ensure main is green and clean (``git status``). Run: ``python scripts/release.py``.
- The script builds CHANGES via Towncrier, optionally pulls/compiles translations, bumps version with ``uv version``, tags (signed if possible), publishes via ``uv publish``, and bumps to next ``X.Y+1.dev0``.

Manual (alternative)
^^^^^^^^^^^^^^^^^^^^
1. Build CHANGES via Towncrier: ``uvx towncrier build --yes --version X.Y.Z``.
2. Bump version in ``pyproject.toml``: ``uv version X.Y.Z``.
3. Commit/tag:
   ::

      git commit -am "Preparing release X.Y.Z"
      git tag -s vX.Y.Z -m "Version X.Y.Z"   # or -a if not signing

4. Build & publish to PyPI:
   ::

      rm -rf dist
      uv build
      uv publish

   To publish to TestPyPI: ``uv publish --index-url https://test.pypi.org/legacy/``.

5. Bump to next dev: ``uv version X.(Y+1).dev0``; commit “Back to development: X.(Y+1)”.

uv keyring setup (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Install keyring: ``uv tool install keyring``.
- Store token: ``keyring set 'https://upload.pypi.org/legacy/' __token__``.
- Export env vars so uv uses the keyring in subprocesses:
  ::

     export UV_KEYRING_PROVIDER=subprocess
     export UV_PUBLISH_USERNAME=__token__

Notes
-----
- Matrix pins live in ``tox.ini``; adjust supported Django/Python there.
- Translations: release script can run ``tx pull`` + ``compilemessages`` and stage ``django_countries/locale``.
