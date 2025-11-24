#!/usr/bin/env python3
"""Django Countries release deployment script.

This script handles the complete release process:
- Updates translations
- Bumps version
- Builds changelog
- Creates git tags
- Publishes to PyPI
- Deploys documentation
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

import click


class DeploymentError(Exception):
    """Raised when deployment fails."""


def run_command(
    cmd: list[str] | str,
    *,
    check: bool = True,
    capture_output: bool = False,
    cwd: Path | None = None,
    dry_run: bool = False,
) -> subprocess.CompletedProcess:
    """Run a shell command with optional dry-run support."""
    if dry_run:
        click.secho(f"   (dry run: would run: {cmd})", fg="yellow", dim=True)
        return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

    if isinstance(cmd, str):
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True,
            cwd=cwd,
        )
    else:
        result = subprocess.run(
            cmd, check=check, capture_output=capture_output, text=True, cwd=cwd
        )
    return result


def check_git_status(allow_dirty: bool = False) -> None:
    """Ensure working directory is clean."""
    if allow_dirty:
        click.secho("⚠ Skipping git status check (--allow-dirty)", fg="yellow")
        return

    result = run_command(["git", "diff-index", "--quiet", "HEAD", "--"], check=False)
    if result.returncode != 0:
        raise DeploymentError(
            "Working directory has uncommitted changes. "
            "Please commit or stash your changes first.\n"
            "Use --allow-dirty to bypass this check (not recommended)."
        )


def pull_latest(dry_run: bool = False) -> None:
    """Pull latest changes from git."""
    click.echo("→ Pulling latest changes...")
    if dry_run:
        # Use git pull --dry-run to show what would be pulled
        result = run_command(
            ["git", "pull", "--dry-run"], capture_output=True, check=False
        )
        if result.stdout.strip():
            click.secho(f"   Would pull: {result.stdout.strip()}", fg="yellow")
        else:
            click.secho("   Already up to date", fg="green")
    else:
        run_command(["git", "pull"])


def update_translation_source(repo_root: Path, dry_run: bool = False) -> None:
    """Update English translation source file."""
    click.echo("→ Updating English translation source file...")

    if dry_run:
        click.secho("   (dry run: skipped)", fg="yellow", dim=True)
        return

    # Run makemessages
    run_command(
        "DJANGO_SETTINGS_MODULE=django_countries.tests.settings "
        "uv run --group dev django-admin makemessages --locale=en --no-obsolete",
        cwd=repo_root / "django_countries",
    )

    # Check if there are changes
    result = run_command(
        ["git", "diff", "--quiet", "django_countries/locale/en/"], check=False
    )

    if result.returncode != 0:  # There are changes
        run_command(["git", "add", "django_countries/locale/en/"])
        run_command(["git", "commit", "-m", "Update English translation source file"])
        click.secho("✓ English source file updated", fg="green")

        click.echo("→ Pushing source strings to Transifex...")
        run_command(["tx", "push", "-s"])
        click.secho("✓ Source strings pushed to Transifex", fg="green")
    else:
        click.secho("✓ No source file changes", fg="green")


def pull_translations(repo_root: Path, dry_run: bool = False) -> None:
    """Pull and compile translations from Transifex."""
    click.echo("→ Pulling translations from Transifex...")

    if dry_run:
        # Show translation status from Transifex
        try:
            result = run_command(["tx", "status"], capture_output=True, check=False)
            if result.returncode == 0 and result.stdout.strip():
                click.secho("   Translation status:", fg="cyan")
                # Show first 15 lines of status
                lines = result.stdout.split("\n")[:15]
                for line in lines:
                    if line.strip():
                        click.echo(f"   {line}")
                if len(result.stdout.split("\n")) > 15:
                    click.secho("   ... (truncated)", dim=True)
            click.secho(
                "   (dry run: would pull and compile translations)",
                fg="yellow",
                dim=True,
            )
        except subprocess.CalledProcessError:
            click.secho(
                "   (dry run: would pull and compile translations)",
                fg="yellow",
                dim=True,
            )
        return

    # Pull from Transifex
    run_command(["tx", "pull", "-a", "--minimum-perc=60", "--use-git-timestamps"])

    # Compile message catalogs
    click.echo("→ Compiling message catalogs (excluding English source)...")
    run_command(
        "uv run --group dev django-admin compilemessages --exclude=en",
        cwd=repo_root / "django_countries",
    )

    # Check if there are changes
    result = run_command(["git", "diff", "--quiet"], check=False)

    if result.returncode != 0:  # There are changes
        run_command(["git", "add", "django_countries/locale"])
        run_command(["git", "commit", "-m", "Update translations from Transifex"])
        click.secho("✓ Translations committed", fg="green")
    else:
        click.secho("✓ No translation changes", fg="green")


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    result = run_command(["uv", "version", "--short"], capture_output=True)
    return result.stdout.strip()


def preview_changelog() -> None:
    """Preview changelog and warn if no fragments."""
    click.echo("→ Previewing changelog...")
    result = run_command(
        [
            "uv",
            "run",
            "--group",
            "dev",
            "towncrier",
            "build",
            "--draft",
            "--version",
            "NEXT",
        ],
        check=False,
        capture_output=True,
    )

    if result.returncode != 0:
        click.secho(
            "⚠ Warning: No changelog fragments found in changes/",
            fg="yellow",
            bold=True,
        )
        if not click.confirm("Continue anyway?"):
            raise DeploymentError("Deployment cancelled by user")


def bump_version(bump_type: str, dry_run: bool = False) -> str:
    """Bump version and return new version."""
    click.echo(f"→ Bumping version ({bump_type})...")

    if dry_run:
        result = run_command(
            ["uv", "version", "--bump", bump_type, "--dry-run"],
            capture_output=True,
        )
        new_version = result.stdout.strip().split()[-1]
    else:
        run_command(["uv", "version", "--bump", bump_type])
        new_version = get_current_version()

    click.secho(f"New version: {new_version}", fg="cyan", bold=True)
    return new_version


def update_doc_markers(
    new_version: str, repo_root: Path, dry_run: bool = False
) -> None:
    """Update documentation version markers."""
    click.echo("→ Updating documentation release markers...")

    target = "New in development version"
    replacement = f"New in version {new_version}"
    files = []
    count = 0

    # Find all markers
    for path in (repo_root / "docs").rglob("*.md"):
        text = path.read_text()
        occurrences = text.count(target)
        if occurrences:
            files.append((path, occurrences))
            count += occurrences

    if count:
        if dry_run:
            click.secho(
                f"~ Would update {count} marker(s) across {len(files)} file(s) "
                f"to '{replacement}'",
                fg="yellow",
            )
            for path, occurrences in files:
                click.echo(f"   - {path.relative_to(repo_root)} ({occurrences})")
        else:
            # Update the files
            for path, _ in files:
                text = path.read_text()
                path.write_text(text.replace(target, replacement))

            click.secho(
                f"✓ Updated {count} marker(s) across {len(files)} file(s)", fg="green"
            )
            for path, _ in files:
                click.echo(f"   - {path.relative_to(repo_root)}")
    else:
        click.secho("✓ No development-version markers found", fg="green")


def run_precommit_checks(dry_run: bool = False) -> None:
    """Run pre-commit checks on version bump."""
    click.echo("→ Running pre-commit checks...")

    # Check if uvx is available
    result = run_command("command -v uvx", check=False, capture_output=True)
    if result.returncode != 0:
        click.secho("   uvx not available, skipping", fg="yellow", dim=True)
        return

    # Stage the file (safe to do even in dry-run)
    if not dry_run:
        run_command(["git", "add", "pyproject.toml"])

    # Run pre-commit checks (safe operation, doesn't commit)
    try:
        run_command(["uvx", "pre-commit", "run", "--files", "pyproject.toml"])
        click.secho("✓ Pre-commit checks passed", fg="green")
    except subprocess.CalledProcessError as e:
        if dry_run:
            click.secho("⚠ Pre-commit checks would fail", fg="yellow")
        else:
            raise DeploymentError("Pre-commit checks failed on pyproject.toml") from e


def build_package(dry_run: bool = False) -> None:
    """Build package to verify everything works."""
    click.echo("→ Building package (verification)...")

    # Clean dist directory
    run_command("rm -rf dist", check=False)

    try:
        run_command(["uv", "build"])
        click.secho("✓ Package built successfully", fg="green")
        if dry_run:
            click.secho("   (cleaning up build artifacts)", fg="yellow", dim=True)
            run_command("rm -rf dist", check=False)
    except subprocess.CalledProcessError as e:
        if dry_run:
            raise DeploymentError(
                "Package build failed in dry-run. "
                "Please fix the issues before deploying."
            ) from e
        raise DeploymentError(
            "Package build failed. Please fix the issues and try again."
        ) from e


def build_and_commit_changelog(new_version: str, dry_run: bool = False) -> None:
    """Build changelog and commit atomically."""
    click.echo("→ Building changelog...")

    # Get today's date in the format "24 November 2025"
    today = datetime.now().strftime("%-d %B %Y")

    if dry_run:
        # Show what the changelog would look like
        click.secho(
            f"   Changelog preview for version {new_version} ({today}):", fg="cyan"
        )
        result = run_command(
            [
                "uv",
                "run",
                "--group",
                "dev",
                "towncrier",
                "build",
                "--version",
                new_version,
                "--date",
                today,
                "--draft",
            ],
            capture_output=True,
            check=False,
        )

        if result.stdout:
            # Print first 30 lines of changelog
            lines = result.stdout.split("\n")
            preview_lines = lines[:30]
            for line in preview_lines:
                click.echo(f"   {line}")
            if len(lines) > 30:
                click.secho(f"   ... ({len(lines) - 30} more lines)", dim=True)
        click.secho("   (dry run: would commit changes)", fg="yellow", dim=True)
        return

    # Build changelog
    run_command(
        [
            "uv",
            "run",
            "--group",
            "dev",
            "towncrier",
            "build",
            "--version",
            new_version,
            "--date",
            today,
            "--yes",
        ]
    )

    # Commit everything
    run_command(["git", "add", "pyproject.toml", "CHANGES.md", "changes/", "docs"])
    run_command(["git", "commit", "-m", f"Preparing release {new_version}"])
    click.secho("✓ Version bump and changelog committed", fg="green")


def create_and_push_tag(new_version: str, dry_run: bool = False) -> None:
    """Create git tag and push."""
    tag_name = f"v{new_version}"

    if dry_run:
        click.echo(f"→ Would create git tag {tag_name}")

        # Check what would be pushed for tags
        click.echo("→ Checking what would be pushed...")
        result = run_command(
            ["git", "push", "--tags", "--dry-run"], capture_output=True, check=False
        )
        if result.stderr:
            # git push outputs to stderr even on success
            for line in result.stderr.split("\n"):
                if line.strip():
                    click.echo(f"   {line}")

        # Check what would be pushed for branch
        result = run_command(
            ["git", "push", "--dry-run"], capture_output=True, check=False
        )
        if result.stderr:
            for line in result.stderr.split("\n"):
                if line.strip():
                    click.echo(f"   {line}")

        click.secho("   (dry run: not pushing)", fg="yellow", dim=True)
        return

    click.echo(f"→ Creating git tag {tag_name}...")
    run_command(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"])
    run_command(["git", "push", "--tags"])
    run_command(["git", "push"])
    click.secho("✓ Tag pushed", fg="green")


def publish_to_pypi(new_version: str, dry_run: bool = False) -> None:
    """Build final package and publish to PyPI."""
    if dry_run:
        click.echo("→ Would build final package and publish to PyPI")

        # Check if package already exists on PyPI
        click.echo(f"   Checking if version {new_version} exists on PyPI...")

        result = run_command(
            f"curl -s -o /dev/null -w '%{{http_code}}' https://pypi.org/pypi/django-countries/{new_version}/json",
            capture_output=True,
            check=False,
        )

        if result.stdout.strip() == "200":
            click.secho(
                f"   ⚠ Version {new_version} already exists on PyPI!",
                fg="yellow",
                bold=True,
            )
        else:
            click.secho(
                f"   ✓ Version {new_version} does not exist on PyPI", fg="green"
            )

        click.secho("   (dry run: not publishing)", fg="yellow", dim=True)
        return

    click.echo("→ Building final package...")
    run_command("rm -rf dist", check=False)
    run_command(["uv", "build"])

    click.echo("→ Publishing to PyPI...")
    run_command(["uv", "publish"])


def deploy_documentation(dry_run: bool = False) -> None:
    """Deploy documentation to GitHub Pages."""
    click.echo("→ Building documentation...")

    if dry_run:
        # Build docs locally to verify they work
        try:
            run_command(["uv", "run", "--group", "docs", "mkdocs", "build", "--strict"])
            click.secho("✓ Documentation builds successfully", fg="green")
            click.secho(
                "   (dry run: would deploy to GitHub Pages)", fg="yellow", dim=True
            )
            # Clean up
            run_command("rm -rf site", check=False)
        except subprocess.CalledProcessError as e:
            raise DeploymentError("Documentation build failed") from e
        return

    click.echo("→ Deploying documentation to GitHub Pages...")
    run_command(["uv", "run", "--group", "docs", "mkdocs", "gh-deploy", "--force"])
    click.secho("✓ Documentation deployed", fg="green")


@click.command()
@click.argument(
    "bump",
    type=click.Choice(["patch", "minor", "major"], case_sensitive=False),
    required=False,
)
@click.option(
    "--dry-run",
    is_flag=True,
    envvar="DRY_RUN",
    help="Run in dry-run mode without making changes",
)
@click.option(
    "--allow-dirty",
    is_flag=True,
    help="Allow deployment with uncommitted changes (not recommended)",
)
def deploy(bump: str | None, dry_run: bool, allow_dirty: bool) -> None:
    """Deploy a new release to PyPI.

    BUMP: Version bump type (patch, minor, or major).
          If not provided, you'll be prompted.

    This command handles the complete release process:
    - Updates English translation source file
    - Pulls and compiles translations from Transifex
    - Bumps version in pyproject.toml
    - Updates documentation version markers
    - Builds changelog from fragments
    - Creates and pushes git tag
    - Publishes to PyPI
    - Deploys documentation to GitHub Pages

    Set DRY_RUN=1 environment variable to preview changes without making them.
    """
    repo_root = Path(__file__).parent.parent.resolve()

    if dry_run:
        click.secho(
            "⚠ DRY RUN MODE ENABLED — no changes will be made", fg="yellow", bold=True
        )
        click.echo()

    click.secho("=" * 38, fg="cyan")
    click.secho("django-countries Release Process", fg="cyan", bold=True)
    click.secho("=" * 38, fg="cyan")
    click.echo()

    # Pre-flight check - verify git status before doing anything else
    try:
        check_git_status(allow_dirty=allow_dirty)
    except DeploymentError as e:
        click.echo()
        click.secho(f"❌ Error: {e}", fg="red", bold=True)
        sys.exit(1)

    # If bump type not provided, prompt for it
    if bump is None:
        current_version = get_current_version()
        click.echo(f"Current version: {current_version}")
        click.echo()

        # Calculate what each bump type would be
        patch_version = (
            run_command(
                ["uv", "version", "--bump", "patch", "--dry-run"], capture_output=True
            )
            .stdout.strip()
            .split()[-1]
        )

        minor_version = (
            run_command(
                ["uv", "version", "--bump", "minor", "--dry-run"], capture_output=True
            )
            .stdout.strip()
            .split()[-1]
        )

        major_version = (
            run_command(
                ["uv", "version", "--bump", "major", "--dry-run"], capture_output=True
            )
            .stdout.strip()
            .split()[-1]
        )

        click.echo("Which version bump do you want?")
        click.echo(f"  1. patch  ({current_version} → {patch_version})  - Bug fixes")
        click.echo(f"  2. minor  ({current_version} → {minor_version})  - New features")
        click.echo(
            f"  3. major  ({current_version} → {major_version})  - Breaking changes"
        )
        click.echo()

        choice = click.prompt(
            "Select version bump",
            type=click.Choice(["1", "2", "3", "patch", "minor", "major"]),
            show_choices=False,
        )

        # Map choice to bump type
        bump_map = {
            "1": "patch",
            "2": "minor",
            "3": "major",
            "patch": "patch",
            "minor": "minor",
            "major": "major",
        }
        bump = bump_map[choice]

        click.echo()
        click.secho("=" * 38, fg="cyan")
        click.echo()

    try:
        pull_latest(dry_run=dry_run)
        click.echo()

        # Translations
        update_translation_source(repo_root, dry_run=dry_run)
        click.echo()

        pull_translations(repo_root, dry_run=dry_run)
        click.echo()

        # Version info
        current_version = get_current_version()
        click.echo(f"Current version: {current_version}")

        preview_changelog()
        click.echo()

        # Version bump
        new_version = bump_version(bump, dry_run=dry_run)
        click.echo()

        # Update docs
        update_doc_markers(new_version, repo_root, dry_run=dry_run)
        click.echo()

        # Pre-commit
        run_precommit_checks(dry_run=dry_run)
        click.echo()

        # Build verification
        build_package(dry_run=dry_run)
        click.echo()

        # Changelog
        build_and_commit_changelog(new_version, dry_run=dry_run)
        click.echo()

        # Tag and push
        create_and_push_tag(new_version, dry_run=dry_run)
        click.echo()

        # Publish
        publish_to_pypi(new_version, dry_run=dry_run)
        click.echo()

        # Documentation
        deploy_documentation(dry_run=dry_run)
        click.echo()

        # Success! Show summary of completed steps
        click.secho("=" * 50, fg="cyan" if dry_run else "green")
        if dry_run:
            click.secho("✓ Dry Run Complete", fg="yellow", bold=True)
        else:
            click.secho(f"✓ Release {new_version} Published!", fg="green", bold=True)
        click.secho("=" * 50, fg="cyan" if dry_run else "green")
        click.echo()

        # Summary of steps
        click.secho("Steps completed:", bold=True)
        click.echo()

        if dry_run:
            steps = [
                ("✓", "Verified git repository is up to date"),
                ("✓", f"Calculated version bump: {current_version} → {new_version}"),
                ("✓", "Previewed changelog with towncrier"),
                ("✓", "Validated documentation markers update"),
                ("✓", "Ran pre-commit checks"),
                ("✓", "Built and validated package"),
                ("✓", "Verified package build succeeds"),
                ("✓", f"Confirmed version {new_version} doesn't exist on PyPI"),
                ("✓", "Validated documentation builds successfully"),
                ("⚠", "Did NOT modify any files", "yellow"),
                ("⚠", "Did NOT create git tags or commits", "yellow"),
                ("⚠", "Did NOT publish to PyPI", "yellow"),
            ]
        else:
            steps = [
                ("✓", "Updated git repository"),
                ("✓", "Updated English translation source file"),
                ("✓", "Pulled and compiled translations from Transifex"),
                ("✓", f"Bumped version: {current_version} → {new_version}"),
                ("✓", "Updated documentation version markers"),
                ("✓", "Ran pre-commit checks"),
                ("✓", "Built and verified package"),
                ("✓", "Built changelog and committed changes"),
                ("✓", f"Created and pushed git tag v{new_version}"),
                ("✓", f"Published version {new_version} to PyPI"),
                ("✓", "Deployed documentation to GitHub Pages"),
            ]

        for item in steps:
            if len(item) == 3:
                icon, text, color = item
                click.secho(f"  {icon} {text}", fg=color)
            else:
                icon, text = item
                click.secho(f"  {icon} {text}", fg="green")

        click.echo()

        if dry_run:
            click.secho("To perform the actual release, run without DRY_RUN:", dim=True)
            click.secho(f"  just deploy {bump}", fg="cyan")
        else:
            click.secho("Next steps:", bold=True)
            click.echo(
                f"  • View release: https://github.com/SmileyChris/django-countries/releases/tag/v{new_version}"
            )
            click.echo(
                f"  • View on PyPI: https://pypi.org/project/django-countries/{new_version}/"
            )
            click.echo("  • View docs: https://django-countries.readthedocs.io/")

        click.echo()

    except DeploymentError as e:
        click.echo()
        click.secho(f"❌ Error: {e}", fg="red", bold=True)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        click.echo()
        click.secho(f"❌ Command failed: {e.cmd}", fg="red", bold=True)
        if e.stderr:
            click.echo(e.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo()
        click.secho("❌ Deployment cancelled by user", fg="red", bold=True)
        sys.exit(1)


if __name__ == "__main__":
    deploy()
