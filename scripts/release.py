#!/usr/bin/env python3
"""
Lightweight release helper that mimics the old zest.releaser flow using uv.

Steps:
1) Pre-flight checks (tools, clean git)
2) Prompt for release version
3) Build changelog via towncrier (from fragments)
4) Optional: pull/compile translations (tx + Django compilemessages)
5) Set version (pyproject) via `uv version`
5) Commit + tag (signed if possible)
6) Publish via `uv publish` (optionally TestPyPI first)
7) Bump to next dev version and add new CHANGES.rst section
"""

from __future__ import annotations

import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
CHANGES = ROOT / "CHANGES.rst"
CHANGES_DIR = ROOT / "changes"
PKG_DIR = ROOT / "django_countries"


def sh(cmd: list[str], check: bool = True, capture: bool = False, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, cwd=cwd or ROOT, text=True, capture_output=capture)


def which(tool: str) -> bool:
    from shutil import which as _which

    return _which(tool) is not None


def assert_clean_git() -> None:
    out = sh(["git", "status", "--porcelain"], capture=True).stdout.strip()
    if out:
        print("Git working tree is not clean. Commit or stash changes first.")
        sys.exit(1)


def get_current_version() -> str:
    text = PYPROJECT.read_text(encoding="utf8")
    m = re.search(r"^version\s*=\s*\"([^\"]+)\"", text, flags=re.M)
    if not m:
        print("Could not find version in pyproject.toml")
        sys.exit(1)
    return m.group(1)


def uv_set_version(version: str) -> None:
    try:
        sh(["uv", "version", version])
    except Exception:
        # Fallback: in-place edit
        text = PYPROJECT.read_text(encoding="utf8")
        text = re.sub(r"^(version\s*=\s*\")[^\"]+(\")", rf"\1{version}\2", text, flags=re.M)
        PYPROJECT.write_text(text, encoding="utf8")


def build_changelog(version: str) -> None:
    """Render CHANGES.rst from towncrier fragments for this version."""
    if not CHANGES_DIR.exists():
        # No fragments directory; skip
        print("No 'changes/' directory found; skipping towncrier.")
        return
    cmd = None
    if which("towncrier"):
        cmd = ["towncrier", "build", "--yes", "--version", version]
    elif which("uvx"):
        cmd = ["uvx", "towncrier", "build", "--yes", "--version", version]
    else:
        print("towncrier not available (install with `uvx pip install towncrier`); skipping changelog build.")
        return
    sh(cmd)


def compute_next_dev(released: str) -> str:
    parts = released.split(".")
    # bump minor (levels=2 style)
    if len(parts) >= 2:
        major, minor = int(parts[0]), int(parts[1])
        return f"{major}.{minor + 1}.dev0"
    # fallback: append .dev0
    return f"{released}.dev0"


def maybe_translations() -> None:
    ans = input("Pull translations from Transifex and compile? [Y/n] ").strip().lower()
    if ans and ans not in {"y", "yes"}:
        return
    if not which("tx"):
        print("tx not found; skipping translation pull.")
    else:
        sh(["tx", "pull", "-a", "--minimum-perc=60"])  # best-effort
    try:
        import django  # noqa: F401
        from django.core.management import call_command

        os.chdir(PKG_DIR)
        try:
            call_command("compilemessages")
        finally:
            os.chdir(ROOT)
        sh(["git", "add", "django_countries/locale"])  # stage locales
    except Exception:
        print("Django not available; skipping compilemessages.")


def main() -> None:
    if not which("uv"):
        print("uv is required. Install with: pipx install uv")
        sys.exit(1)
    if not which("git"):
        print("git is required")
        sys.exit(1)
    assert_clean_git()

    current = get_current_version()
    print(f"Current version: {current}")
    release = input("Release version (e.g., 7.7 or 7.7.1): ").strip()
    if not release:
        print("Aborted: no version provided")
        sys.exit(1)

    build_changelog(release)
    maybe_translations()

    uv_set_version(release)
    sh(["git", "commit", "-am", f"Preparing release {release}"])

    # Tag signed if possible
    try:
        sh(["git", "tag", "-s", f"v{release}", "-m", f"Version {release}"])
    except Exception:
        sh(["git", "tag", "-a", f"v{release}", "-m", f"Version {release}"])

    # Publish
    idx = input("Publish to (p)ypi, (t)estpypi, or (s)kip? [p/t/s]: ").strip().lower()
    if idx == "t":
        sh(["uv", "publish", "--index-url", "https://test.pypi.org/legacy/"])
    elif idx == "p" or idx == "":
        sh(["uv", "publish"])  # expects token or configured credentials
    else:
        print("Skipping publish.")

    # Bump to next dev
    next_dev = compute_next_dev(release if "." in release else f"{release}.0")
    uv_set_version(next_dev)
    sh(["git", "commit", "-am", f"Back to development: {next_dev.split('.dev', 1)[0]}"])

    # Push
    push = input("Push commits and tags to origin? [Y/n] ").strip().lower()
    if not push or push in {"y", "yes"}:
        sh(["git", "push", "--follow-tags"])

    print(f"Released {release} and bumped to {next_dev}.")


if __name__ == "__main__":
    main()
