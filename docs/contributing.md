# Contributing to django-countries

Thank you for considering contributing to django-countries!

## 🌍 Contributing Translations

**Want to help translate country names?** Visit our [Transifex project](https://explore.transifex.com/smileychris/django-countries/) to contribute translations. No coding required!

Country names are translated using Django's standard i18n system. All translation work is done through Transifex, making it easy for anyone to contribute translations in their language.

## Development Setup

The rest of this guide covers code contributions. If you're contributing translations, head to Transifex instead!

This project uses modern Python tooling:
- **uv** - Fast Python package manager and runner
- **just** - Command runner for common development tasks
- **ruff** - Fast all-in-one linter and formatter

### Prerequisites

1. **Install uv** (Python package manager)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or see [uv installation docs](https://github.com/astral-sh/uv#installation)

2. **Install just** (command runner)
   ```bash
   # macOS
   brew install just

   # Linux (using cargo)
   cargo install just

   # Or download from: https://github.com/casey/just
   ```

### Quick Start

```bash
# Set up development environment
uv sync

# Run all tests and coverage
just test

# Run all checks (format, lint, type, docs, tests)
just check
```

## Available Commands

See all commands:
```bash
just --list
```

### Testing

```bash
# Run all test environments (Python 3.8-3.13, Django 3.2-5.2)
just test

# Quick test with current Python (no coverage matrix)
just test quick

# Run specific environment
just test [latest|previous|legacy|latest-pyuca|latest-noi18n]

# Examples:
just test latest           # Latest Django/DRF with Python 3.13
just test previous         # Django 4.2 with Python 3.10
just test legacy           # Django 3.2 with Python 3.8

# Run specific environment with custom Python version
just test [latest|previous|legacy|latest-pyuca|latest-noi18n] [3.8-3.13]

# Examples:
just test latest 3.12      # Latest Django with Python 3.12
just test previous 3.9     # Django 4.2 with Python 3.9
```

Test environments:
- **legacy**: Python 3.8 + Django 3.2 + DRF 3.11
- **previous**: Python 3.10 + Django 4.2 + DRF 3.14
- **latest**: Python 3.13 + Django 5.2 + DRF 3.15
- **latest-pyuca**: Latest + pyuca (Unicode collation)
- **latest-noi18n**: Latest + i18n disabled

Coverage is automatically generated when running `just test`.

### Code Quality

The `just check` command runs all quality checks (formatting, linting, type checking, docs, and tests).

For individual checks, you can run the tools directly:

```bash
# Format code (import sorting + formatting)
uv run ruff check --select I --fix django_countries
uv run ruff format django_countries

# Check formatting without changes
uv run ruff check --select I django_countries
uv run ruff format --check django_countries

# Run linters
uv run ruff check django_countries
uv run bandit -r django_countries -x tests

# Type checking
uv run mypy django_countries
```

### Development Workflow

1. **Make changes** to the code
2. **Run tests**: `just test quick` (fastest) or `just test latest` (single env) or `just test` (full matrix)
3. **Check everything**: `just check` (runs all checks)
4. **Commit** your changes

### Pre-commit Hooks

Optional but recommended:

```bash
# Install pre-commit hooks
uvx pre-commit install

# Run hooks manually on all files
uvx pre-commit run --all-files
```

## Testing

Tests are in `django_countries/tests/`:
- `test_fields.py` - CountryField model field tests
- `test_countries.py` - Countries class tests
- `test_drf.py` - Django REST Framework integration
- `test_admin_filters.py` - Admin filter tests
- `test_widgets.py` - Widget rendering tests
- `test_tags.py` - Template tag tests
- `graphql/` - GraphQL integration tests

### Coverage Requirements

- **Tests**: 100% coverage required
- **Source code**: 90% coverage required

Coverage is generated automatically when running `just test`. View the report by opening `htmlcov/index.html` in your browser.

## Code Style

This project uses:
- **ruff** for linting, import sorting, and formatting
- **mypy** for type checking
- **bandit** for security scanning

The pre-commit hooks will automatically enforce style. You can also run `just check` to verify all style requirements.

## Migration from Tox

If you previously used `tox`, here's the command mapping:

| Old (tox) | New (uv/just) |
|-----------|------------|
| `tox` | `just test` |
| `tox -e py311-latest` | `just test latest 3.11` |
| `tox -e mypy` | `uv run mypy django_countries` |
| `tox -e bandit` | `uv run bandit -r django_countries -x tests` |
| `tox -e readme` | `uv run --group docs mkdocs build --strict` |
| `black .` | `uv run ruff format django_countries` |

## Releasing (for Maintainers)

### Prerequisites

Before releasing, ensure you have:
- Your PyPI credentials in your keyring and the `keyring` tool installed (see setup below)
- The Transifex CLI installed (see installation instructions below)

### 🗺️ Updating Country Data

Country data should be manually updated from the official ISO 3166-1 Online Browsing Platform (OBP) when changes occur:

1. Visit: https://www.iso.org/obp/ui/
2. Click the 'Country Codes' radio button
3. Click the search button (🔍)
4. Change 'Results per page' to 300
5. Select and copy the table data
6. Paste into a spreadsheet (LibreOffice Calc, Excel, etc.)
7. Verify columns: Country Name, Alpha-2, Alpha-3, Numeric
8. Delete any extra columns (like French names)
9. Delete the header row
10. Save as `django_countries/iso3166-1.csv`
11. Run: `uv run --group dev python django_countries/data.py` to regenerate `data.py`

The official OBP data uses specific formatting patterns documented in [ISO 3166-1 Country Name Formatting](iso3166-formatting.md).

### Quick Release (Recommended)

The `just deploy [patch|minor|major]` command handles the entire release process (bump type required):

```bash
# For a patch release (bug fixes: 7.7.0 -> 7.7.1)
just deploy patch

# For a minor release (new features: 7.7.0 -> 7.8.0)
just deploy minor

# For a major release (breaking changes: 7.7.0 -> 8.0.0)
just deploy major
```

This will:
1. Check for uncommitted changes (must have clean working directory)
2. Pull latest changes from git
3. Pull and compile translations from Transifex
4. Commit translation updates (if any)
5. Preview changelog to verify fragments exist
6. Bump version in pyproject.toml
7. Run pre-commit checks on version bump
8. Build package to verify everything works
9. Build changelog from fragments and commit atomically
10. Create and push git tag
11. Build final package and publish to PyPI
12. Deploy documentation to GitHub Pages

**Note**: Add changelog entries to `changes/` directory before releasing. See `changes/README.md` for details.

### Choosing the Right Release Type

This project follows [Semantic Versioning](https://semver.org/):

- **Patch (X.Y.Z)**: Bug fixes, translations, flag updates, documentation fixes
- **Minor (X.Y.0)**: New features, new Django/Python/DRF support, country name changes, performance improvements
- **Major (X.0.0)**: Breaking changes, dropping Python/Django support, API changes, removing deprecated features

**Key Rule**: Adding version support = minor. Dropping version support = major.

After the release, remember to bump to the next development version:

```bash
uv version --bump minor
# Manually edit pyproject.toml to change version from X.Y.0 to X.Y.dev0
git add pyproject.toml
git commit -m "Back to development: X.Y.dev0"
git push
```

### Manual Release

If you prefer manual control, you can do each step individually:

**1. Prepare translations**

```bash
just tx-pull
git add django_countries/locale
git commit -m "Update translations from Transifex"
```

**2. Bump version**

```bash
uv version --bump patch   # or minor/major
```

**3. Build changelog**

```bash
uv run --group dev towncrier build --version $(uv version --short) --date "$(date '+%-d %B %Y')" --yes
```

**4. Commit and tag**

```bash
git add pyproject.toml CHANGES.md changes/
git commit -m "Preparing release $(uv version --short)"
git tag -a v$(uv version --short) -m "Release v$(uv version --short)"
git push --tags
git push
```

**5. Build and publish**

```bash
rm -rf dist
uv build
uv publish
```

### Setting Up PyPI Credentials

Install keyring (used by uv for publishing) and set your credentials:

```bash
uv tool install keyring
keyring set 'https://upload.pypi.org/legacy/' __token__
```

Next, add these environment variables (e.g., in your `~/.bashrc` or `~/.zshrc`):

```bash
export UV_KEYRING_PROVIDER=subprocess
export UV_PUBLISH_USERNAME=__token__
```

### Installing Transifex CLI

The Transifex CLI is required for pulling translations before a release:

```bash
# Install using the official installer
curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | bash
```

See the [Transifex CLI documentation](https://github.com/transifex/cli) for alternative installation methods.

## Getting Help

- Check `just --list` for available commands
- See the [documentation](index.md) for project information
- Open an issue on GitHub for questions or problems

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add a changelog entry in `changes/` (see `changes/README.md`)
5. Run `just check` to ensure all checks pass
6. Submit a pull request

All PRs must pass CI checks (formatting, linting, type checking, tests).

### Adding Changelog Entries

For changes that should appear in the release notes, create a file in the `changes/` directory:

```bash
# With issue/PR number
echo "Your change description" > changes/123.bugfix.rst

# Without issue/PR (prefix with +)
echo "Your change description" > changes/+20250104.misc.rst
```

Types: `feature`, `bugfix`, `doc`, `removal`, `misc`

See `changes/README.md` for full details.
