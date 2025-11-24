# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**django-countries** is a Django application that provides country choices for use with forms, flag icons static files, and a country field for models. It provides all ISO 3166-1 countries as choices with support for translations via Django's gettext.

## Development Commands

This project uses **uv** (fast package manager) and **just** (command runner). See `docs/contributing.md` for setup instructions.

### Testing
```bash
# Run all test environments + coverage (recommended)
just test

# Quick test with current Python (no coverage matrix)
just test quick

# Run specific test environment
just test [latest|previous|legacy|latest-pyuca|latest-noi18n]

# Examples:
just test latest           # Python 3.13 + Django 5.2
just test previous         # Python 3.10 + Django 4.2
just test legacy           # Python 3.8 + Django 3.2
just test latest-pyuca     # With Unicode collation
just test latest-noi18n    # Without i18n

# Run specific environment with custom Python version
just test [latest|previous|legacy|latest-pyuca|latest-noi18n] [3.8-3.13]

# Example:
just test latest 3.12      # Latest Django with Python 3.12

# Run a single test file
uv run --group test pytest django_countries/tests/test_fields.py

# Run a specific test
uv run --group test pytest django_countries/tests/test_fields.py::TestCountryField::test_name
```

### Code Quality
```bash
# Run ALL checks (format, lint, type, docs, tests)
just check

# Run individual tools directly
uv run ruff format django_countries           # Format code
uv run ruff check django_countries            # Lint code
uv run mypy django_countries                  # Type check
uv run bandit -r django_countries -x tests    # Security scan
```

### Coverage
Coverage is automatically generated when running `just test`. View the HTML report at `htmlcov/index.html`.

### Documentation
```bash
just docs  # Serve documentation locally at http://127.0.0.1:8080
```

Documentation is built with MkDocs and automatically deployed to GitHub Pages during `just deploy`.

### Updating Country Data

Country data should be manually updated from the official ISO 3166-1 Online Browsing Platform (OBP):

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

The official OBP data uses specific formatting (parentheses vs commas) documented in `docs/iso3166-formatting.md`.

### Translation Commands (for Maintainers)
```bash
# Update English source file with new translatable strings (after editing data.py or base.py)
just tx-makemessages

# Pull and compile translations from Transifex
just tx-pull
```

**Translation Workflow**:
1. When country names change in `data.py` or `base.py`, run `just tx-makemessages`
2. This generates/updates `django_countries/locale/en/LC_MESSAGES/django.po` (English source)
3. Commit the English source file
4. Push to Transifex with `tx push -s` (done automatically in deploy)
5. Translators update translations on Transifex
6. Pull translations with `just tx-pull`

### Release Commands (for Maintainers)
```bash
# Deploy a release to PyPI (fully automated)
just deploy          # Interactive prompt for version bump
just deploy patch    # For bug fixes (7.7.0 -> 7.7.1)
just deploy minor    # For new features (7.7.0 -> 7.8.0)
just deploy major    # For breaking changes (7.7.0 -> 8.0.0)

# Dry-run mode to preview and validate changes
DRY_RUN=1 just deploy
DRY_RUN=1 just deploy patch

# Allow uncommitted changes (not recommended)
just deploy patch --allow-dirty
DRY_RUN=1 just deploy --allow-dirty
```

The `just deploy [patch|minor|major]` command runs `scripts/deploy.py` (a Python script using click) that handles the entire release process:
- Pulls latest changes
- Updates English translation source file and pushes to Transifex
- Pulls latest translations from Transifex
- Bumps version and builds changelog from `changes/` fragments using towncrier
- Creates git tag and pushes
- Builds and publishes to PyPI
- Deploys documentation to GitHub Pages

**Interactive Mode**: Running `just deploy` without arguments will show an interactive prompt with version options (e.g., "8.1.1 → 8.2.0") to help you choose the right bump type.

**Dry-Run Mode**: The `DRY_RUN=1` environment variable enables dry-run mode that:
- Checks for uncommitted changes (same as real run)
- Actually builds and validates the package
- Builds and validates documentation
- Shows full changelog preview (30 lines)
- Runs pre-commit checks
- Checks if version exists on PyPI
- Shows what would be pushed to git
- Displays translation status from Transifex
- Provides a summary of all steps at the end
- Does NOT modify files, create commits/tags, or publish anything

**Allow Dirty Working Directory**: The `--allow-dirty` flag bypasses the git status check, allowing deployment with uncommitted changes. This is not recommended for production releases but can be useful for testing.

**Changelog Management**: This project uses [towncrier](https://pypi.org/project/towncrier/) for changelog management.

**IMPORTANT**: When making significant changes, **always create a changelog fragment**:

```bash
# If fixing/implementing an issue or PR, use the number:
changes/342.bugfix.md
changes/423.feature.md

# Otherwise, use descriptive unique names:
changes/+20251104-common-names.feature.md
changes/+20251104-iso-docs.doc.md
```

Fragment types: `feature`, `bugfix`, `doc`, `removal`, `misc`

See `changes/README.md` for details.

**One-time setup**: Install Transifex CLI with `curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | bash`

See the "Releasing (for Maintainers)" section in `docs/contributing.md` for the complete release workflow.

## Build System

The project uses **uv_build** as the build backend (uv's native build system for pure Python packages). Configuration in `pyproject.toml`:

```toml
[build-system]
requires = ["uv_build>=0.9.6,<0.10.0"]
build-backend = "uv_build"
```

**Version Management**: Version is stored in `pyproject.toml` and managed using `uv version --bump [major|minor|patch]`.

**Building**: Use `uv build` to create wheel and source distributions, or `just deploy [patch|minor|major]` to build and publish.

## Architecture

### Core Components

**Countries Class (`__init__.py`)**: The central `Countries` class manages the list of available countries. It handles:
- Loading country data from `iso3166-1.csv` and `data.py`
- Applying settings like `COUNTRIES_OVERRIDE`, `COUNTRIES_ONLY`, `COUNTRIES_FIRST`
- Translation of country names with fallback handling
- Optional pyuca sorting for better Unicode collation
- Alternative country codes (alpha3, numeric, IOC)

**Country Object (`fields.py`)**: A lightweight wrapper around a country code that provides:
- Lazy loading of country properties (name, flag, alpha3, numeric, ioc_code)
- Unicode flag emoji via `unicode_flag` property
- Extension points via entry_points mechanism for third-party plugins
- HTML escaping support for safe rendering

**CountryField (`fields.py`)**: A Django model field based on CharField that:
- Stores 2-character ISO country codes (or comma-separated for multiple)
- Supports multiple country selection with `multiple=True`
- Custom lookups: `__name`, `__iname` for filtering by country name
- Integration with Django admin filters via `filters.py`

**Settings (`conf.py`)**: App-specific settings with COUNTRIES_ prefix:
- `COUNTRIES_FLAG_URL`: Template for flag image URLs
- `COUNTRIES_COMMON_NAMES`: Use friendlier names (e.g., "Bolivia" vs "Bolivia, Plurinational State of")
- `COUNTRIES_OVERRIDE`: Override specific country names
- `COUNTRIES_ONLY`: Restrict to specific countries
- `COUNTRIES_FIRST`: Show certain countries at top of list
- `COUNTRIES_FIRST_REPEAT`, `COUNTRIES_FIRST_BREAK`, `COUNTRIES_FIRST_SORT`: Control first-countries behavior

### Integration Points

**Django REST Framework** (`serializers.py`, `serializer_fields.py`):
- `CountryFieldMixin`: Mixin for model serializers with CountryField
- `CountryField` serializer field with configurable output format
- Supports `country_dict=True` for verbose `{code, name}` output
- Supports `name_only=True` for country name output

**GraphQL** (`graphql/`):
- Country object type with schema support for graphene-django
- Provides fields: code, name, alpha3, numeric, iocCode

**Template Tags** (`templatetags/`):
- `{% get_country 'CODE' as var %}` - Get Country object from code
- `{% get_countries %}` - Get full list of countries

**Widgets** (`widgets.py`):
- `CountrySelectWidget`: Select widget with flag image display

### Data Flow

1. Country codes are stored in the database as 2-character strings
2. When accessed via model instances, codes are wrapped in Country objects
3. Country objects lazily load properties from the Countries singleton
4. The Countries singleton applies settings and handles translations
5. Translations use Django's standard gettext with fallback handling

### Testing Structure

Tests are in `django_countries/tests/`:
- `test_fields.py`: CountryField model field tests (most comprehensive)
- `test_countries.py`: Countries class and Country object tests
- `test_drf.py`: Django REST Framework integration tests
- `test_admin_filters.py`: Admin filter tests
- `test_widgets.py`: Widget rendering tests
- `test_tags.py`: Template tag tests
- `graphql/`: GraphQL integration tests
- `settings.py` and `settings_noi18n.py`: Test settings

Test models are defined in `tests/models.py` and the test app is configured in `tests/apps.py`.

## Important Notes

- The package maintains 100% test coverage for tests themselves and 90%+ for main code
- Country names are translated using Django's i18n; test with both i18n enabled and disabled
- Pre-commit hooks enforce: ruff (linting + formatting)
- The project uses modern pyproject.toml-only build with uv_build backend
- Type hints are checked with mypy using django-stubs
- Multiple country selection stores countries as comma-separated string by default (sorted, with duplicates removed)
- The Countries class can be subclassed for per-field customization
- Translations are managed via Transifex and pulled using `just tx-pull`
- Releases use `uv version` for version management and `just deploy` for publishing
- Supported versions:
  - Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
  - Django 3.2 (LTS), 4.2 (LTS), 5.0, 5.1, 5.2
  - DRF 3.11+
