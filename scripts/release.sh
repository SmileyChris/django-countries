#!/usr/bin/env bash

# Lightweight release helper (shell version) mirroring scripts/release.py

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"
PYPROJECT="$ROOT/pyproject.toml"
CHANGES_DIR="$ROOT/changes"
PKG_DIR="$ROOT/django_countries"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" || "${1:-}" == "-n" || "${DRY_RUN:-0}" == "1" ]]; then
  DRY_RUN=1
fi

die() {
  echo "error: $*" >&2
  exit 1
}

have() {
  command -v "$1" >/dev/null 2>&1
}

say() {
  echo "$*"
}

show_cmd() {
  printf '+ %s\n' "$*"
}

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    show_cmd "$*"
  else
    "$@"
  fi
}

runsh() {
  local cmd="$*"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    show_cmd "$cmd"
  else
    bash -lc "$cmd"
  fi
}

assert_clean_git() {
  local out
  out=$(git -C "$ROOT" status --porcelain)
  if [[ -n "$out" ]]; then
    if [[ "$DRY_RUN" -eq 1 ]]; then
      say "note: working tree not clean; proceeding due to dry-run."
    else
      die "Git working tree is not clean. Commit or stash changes first."
    fi
  fi
}

current_version() {
  awk -F'"' '/^version *= *"/ { print $2; exit }' "$PYPROJECT"
}

uv_set_version() {
  local version="$1"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    show_cmd "uv version $version || sed -E -i 's/^version *= *\".*\"/version = \"$version\"/' $PYPROJECT"
    return 0
  fi
  if have uv; then
    if ! (cd "$ROOT" && uv version "$version"); then
      # Fallback to sed in-place edit
      sed -E -i 's/^version *= *".*"/version = '"\"$version\""'/' "$PYPROJECT"
    fi
  else
    sed -E -i 's/^version *= *".*"/version = '"\"$version\""'/' "$PYPROJECT"
  fi
}

build_changelog() {
  local version="$1"
  if [[ ! -d "$CHANGES_DIR" ]]; then
    echo "No 'changes/' directory found; skipping towncrier."
    return 0
  fi
  if have towncrier; then
    runsh "cd '$ROOT' && towncrier build --yes --version '$version'"
  elif have uvx; then
    runsh "cd '$ROOT' && uvx towncrier build --yes --version '$version'"
  else
    echo "towncrier not available (install with 'uvx pip install towncrier'); skipping changelog build."
  fi
}

compute_next_dev() {
  # Bump minor (levels=2 style). For X or X.Y[.Z], use major.minor+1.dev0
  local released="$1"
  local major minor
  IFS='.' read -r major minor _rest <<<"$released"
  if [[ -n "${minor:-}" ]]; then
    echo "${major}.$((minor + 1)).dev0"
  else
    echo "${released}.dev0"
  fi
}

maybe_translations() {
  local ans
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "Would prompt: Pull translations from Transifex and compile? [Y/n] (default: Y)"
    ans="y"
  else
    read -r -p "Pull translations from Transifex and compile? [Y/n] " ans || ans=""
  fi
  ans="${ans,,}"
  if [[ -n "$ans" && "$ans" != "y" && "$ans" != "yes" ]]; then
    return 0
  fi

  if have tx; then
    # Best effort; do not fail the whole script if this fails.
    runsh "cd '$ROOT' && tx pull -a --minimum-perc=60" || echo "tx pull failed; continuing."
  else
    echo "tx not found; skipping translation pull."
  fi

  # Try to compile messages if Django is available
  if python - <<'PY' >/dev/null 2>&1
import django  # noqa: F401
PY
  then
    runsh "cd '$PKG_DIR' && python - <<'PY'
from django.core.management import call_command
call_command('compilemessages')
PY
    " || echo "compilemessages failed; continuing."
    run git -C "$ROOT" add django_countries/locale || true
  else
    echo "Django not available; skipping compilemessages."
  fi
}

main() {
  if ! have uv; then
    if [[ "$DRY_RUN" -eq 1 ]]; then
      say "note: uv not found; required for real run."
    else
      die "uv is required. Install with: pipx install uv"
    fi
  fi
  have git || die "git is required"
  assert_clean_git

  local current release next_dev base_for_next idx msg
  current="$(current_version)"
  echo "Current version: $current"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    # default: strip .dev* if present; otherwise use current
    release="$current"
    if [[ "$release" == *.dev* ]]; then
      release="${release%%.dev*}"
    fi
    say "Would prompt: Release version (e.g., 7.7 or 7.7.1): using '$release'"
  else
    read -r -p "Release version (e.g., 7.7 or 7.7.1): " release || release=""
  fi
  release="${release// /}"
  if [[ -z "$release" ]]; then
    die "Aborted: no version provided"
  fi

  build_changelog "$release"
  maybe_translations

  uv_set_version "$release"
  run git -C "$ROOT" commit -am "Preparing release $release"

  # Tag signed if possible; fall back to annotated
  if ! run git -C "$ROOT" tag -s "v$release" -m "Version $release" 2>/dev/null; then
    run git -C "$ROOT" tag -a "v$release" -m "Version $release"
  fi

  # Publish
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "Would prompt: Publish to (p)ypi, (t)estpypi, or (s)kip? [p/t/s]: default p"
    idx="p"
  else
    read -r -p "Publish to (p)ypi, (t)estpypi, or (s)kip? [p/t/s]: " idx || idx=""
  fi
  idx="${idx,,}"
  if [[ "$idx" == "t" ]]; then
    runsh "cd '$ROOT' && uv publish --index-url https://test.pypi.org/legacy/"
  elif [[ -z "$idx" || "$idx" == "p" ]]; then
    runsh "cd '$ROOT' && uv publish"
  else
    echo "Skipping publish."
  fi

  # Bump to next dev
  if [[ "$release" == *.* ]]; then
    base_for_next="$release"
  else
    base_for_next="$release.0"
  fi
  next_dev="$(compute_next_dev "$base_for_next")"
  uv_set_version "$next_dev"
  msg="Back to development: ${next_dev%%.dev*}"
  run git -C "$ROOT" commit -am "$msg"

  # Push
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "Would prompt: Push commits and tags to origin? [Y/n] default Y"
    ans="y"
  else
    read -r -p "Push commits and tags to origin? [Y/n] " ans || ans=""
  fi
  ans="${ans,,}"
  if [[ -z "$ans" || "$ans" == "y" || "$ans" == "yes" ]]; then
    run git -C "$ROOT" push --follow-tags
  fi

  echo "Released $release and bumped to $next_dev."
}

main "$@"
