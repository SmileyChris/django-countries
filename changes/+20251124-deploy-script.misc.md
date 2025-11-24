Refactored deployment script from bash (244 lines) to Python using click for better maintainability and testability. The script is now in `scripts/deploy.py` with these improvements:

- **Interactive mode**: Run `just deploy` without arguments to get an interactive prompt showing version options (e.g., "8.1.1 → 8.2.0")
- **Enhanced dry-run**: `DRY_RUN=1` now validates package builds, documentation builds, runs pre-commit checks, shows full changelog preview, checks PyPI for existing versions, displays translation status, and checks for uncommitted changes (same as real run)
- **Comprehensive summary**: Shows a detailed list of completed steps at the end of each run
- **Allow dirty**: `--allow-dirty` flag to bypass git status check when needed (not recommended for production)
- **Better error handling**: Clear error messages with proper exception types
- **Colorful output**: Uses click's styling for better readability
