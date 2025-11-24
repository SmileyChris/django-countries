# django-countries justfile - Modern development commands using uv

# Default recipe - show available commands
default:
    @just --list

# Run tests - smart command that handles multiple scenarios
# Usage:
#   just test                                          -> run all test matrices + coverage
#   just test quick                                    -> quick test with current Python (no coverage)
#   just test [latest|previous|legacy|latest-pyuca|latest-noi18n]              -> run specific env
#   just test [latest|previous|legacy|latest-pyuca|latest-noi18n] [3.8-3.13]   -> run specific env + python
test *ARGS='':
    #!/usr/bin/env bash
    set -euo pipefail

    # Pass ARGS from just to bash script
    ARGS=({{ ARGS }})

    if [ ${#ARGS[@]} -eq 0 ]; then
        # No args: run all test matrices + coverage
        echo "Running all test environments..."
        just _test-matrix
        echo ""
        echo "Generating coverage report..."
        just _coverage-report
    elif [ ${#ARGS[@]} -eq 1 ]; then
        # One arg: could be "quick" or environment name
        ENV="${ARGS[0]}"
        if [ "$ENV" = "quick" ]; then
            echo "Running quick test with current Python..."
            uv run --group test pytest
        else
            case "$ENV" in
                legacy)      PYTHON="3.8" ;;
                previous)    PYTHON="3.10" ;;
                latest|latest-pyuca|latest-noi18n) PYTHON="3.13" ;;
                *)           echo "Unknown environment: $ENV"; exit 1 ;;
            esac
            just _test-env "$ENV" "$PYTHON"
        fi
    elif [ ${#ARGS[@]} -eq 2 ]; then
        # Two args: environment and python version
        just _test-env "${ARGS[0]}" "${ARGS[1]}"
    else
        echo "Usage: just test [ENV [PYTHON]]"
        exit 1
    fi

# Run all test environments (internal)
_test-matrix:
    @echo "Cleaning old coverage files..."
    @rm -rf .coverage* htmlcov
    @just _test-env legacy 3.8
    @just _test-env previous 3.10
    @just _test-env latest 3.13
    @just _test-env latest-pyuca 3.13
    @just _test-env latest-noi18n 3.13

# Run a specific test environment (internal)
_test-env ENV PYTHON:
    @echo ""
    @echo "========================================="
    @echo "Testing: Python {{ PYTHON }} - {{ ENV }}"
    @echo "========================================="
    @case "{{ ENV }}" in \
        legacy) \
            uv run --python {{ PYTHON }} \
                   --with "Django==3.2.*" \
                   --with "djangorestframework==3.11.*" \
                   --with "pyuca" \
                   --group test \
                   coverage run -m pytest \
            ;; \
        previous) \
            uv run --python {{ PYTHON }} \
                   --with "Django==4.2.*" \
                   --with "djangorestframework==3.14.*" \
                   --group test \
                   coverage run -m pytest \
            ;; \
        latest) \
            uv run --python {{ PYTHON }} \
                   --with "Django==5.1.*" \
                   --with "djangorestframework==3.15.*" \
                   --with "graphene-django==3.0.*" \
                   --group test \
                   coverage run -m pytest \
            ;; \
        latest-pyuca) \
            uv run --python {{ PYTHON }} \
                   --with "Django==5.1.*" \
                   --with "djangorestframework==3.15.*" \
                   --with "graphene-django==3.0.*" \
                   --with "pyuca" \
                   --group test \
                   coverage run -m pytest \
            ;; \
        latest-noi18n) \
            DJANGO_SETTINGS_MODULE=django_countries.tests.settings_noi18n \
            uv run --python {{ PYTHON }} \
                   --with "Django==5.1.*" \
                   --with "djangorestframework==3.15.*" \
                   --with "graphene-django==3.0.*" \
                   --group test \
                   coverage run -m pytest \
            ;; \
        *) \
            echo "Unknown environment: {{ ENV }}"; exit 1 \
            ;; \
    esac

# Generate coverage report (internal)
_coverage-report:
    @uv run --group test coverage combine .coverage* 2>/dev/null || true
    @echo ""
    @echo "Test coverage (must be 100%):"
    @uv run --group test coverage report --include="django_countries/tests/*" --fail-under=100 -m
    @echo ""
    @echo "Source coverage (must be 90%+):"
    @uv run --group test coverage report --omit="django_countries/tests/*" --fail-under=90 -m
    @uv run --group test coverage html
    @echo ""
    @echo "Coverage report saved to htmlcov/index.html"

# Run all checks (format, lint, type, docs, test)
check:
    @echo "Running all checks..."
    @echo ""
    @echo "→ Checking code formatting..."
    uv run ruff check --select I django_countries
    uv run ruff format --check django_countries
    @echo "✓ Formatting OK"
    @echo ""
    @echo "→ Running linters..."
    uv run ruff check django_countries
    uv run bandit -r django_countries -x tests
    @echo "✓ Linting OK"
    @echo ""
    @echo "→ Type checking..."
    uv run mypy django_countries
    @echo "✓ Type checking OK"
    @echo ""
    @echo "→ Validating documentation..."
    uv run --group docs mkdocs build --strict
    @echo "✓ Documentation OK"
    @echo ""
    @echo "→ Running tests..."
    just test
    @echo ""
    @echo "======================================"
    @echo "✓ All checks passed!"
    @echo "======================================"

# Serve documentation locally at http://127.0.0.1:8080
docs:
    uv run --group docs mkdocs serve --livereload --dev-addr 127.0.0.1:8080

# Build and deploy documentation to GitHub Pages
deploy_docs:
    @echo "Building documentation..."
    uv run --group docs mkdocs build --strict
    @echo "✓ Documentation builds successfully"
    @echo ""
    @echo "Deploying to GitHub Pages..."
    uv run --group docs mkdocs gh-deploy --force
    @echo "✓ Documentation deployed"

# Update English translation source file with new translatable strings
tx-makemessages:
    @echo "Updating English translation source file..."
    @cd django_countries && DJANGO_SETTINGS_MODULE=django_countries.tests.settings \
        uv run --group dev django-admin makemessages --locale=en --no-obsolete
    @echo "✓ English source file updated (django_countries/locale/en/LC_MESSAGES/django.po)"
    @echo ""
    @echo "Next steps:"
    @echo "  1. Review changes: git diff django_countries/locale/en/"
    @echo "  2. Commit changes: git add django_countries/locale/en/ && git commit -m 'Update English translation source file'"
    @echo "  3. Push source to Transifex: tx push -s"
    @echo "  4. Wait for translators to update translations on Transifex"
    @echo "  5. Pull updated translations: just tx-pull"

# Pull translations from Transifex and compile message catalogs
tx-pull:
    @echo "Pulling translations from Transifex..."
    tx pull -a --minimum-perc=60 --use-git-timestamps
    @echo "Compiling message catalogs (excluding English source)..."
    @cd django_countries && uv run --group dev django-admin compilemessages --exclude=en
    @echo "✓ Translations updated and compiled"

# Deploy a new release to PyPI
# Usage:
#   just deploy [patch|minor|major]  - Specify bump type
#   just deploy                       - Interactive prompt for bump type
#   just deploy [BUMP] --allow-dirty - Allow uncommitted changes (not recommended)
deploy *ARGS:
    uv run --group dev python scripts/deploy.py {{ ARGS }}
