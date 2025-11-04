# Changelog Fragments

This directory contains changelog fragments for [towncrier](https://pypi.org/project/towncrier/).

## Adding a changelog entry

When you make a change that should be included in the changelog, create a file in this directory named:

```
<issue_or_pr_number>.<type>.md
```

Where `<type>` is one of:

- **feature** - New features and enhancements
- **bugfix** - Bug fixes
- **doc** - Documentation improvements
- **removal** - Deprecations and removals
- **misc** - Miscellaneous changes (not shown in changelog)

### Examples

```bash
# Feature from PR #123
echo "Add support for custom country codes" > changes/123.feature.md

# Bug fix from issue #456
echo "Fix TypeError in CountryFilter.choices()" > changes/456.bugfix.md

# If there's no issue/PR number, prefix with + and use a unique identifier
echo "Update development tooling" > changes/+20250104.misc.md
```

## Building the changelog

During the release process, `just deploy` will automatically run:

```bash
towncrier build --version X.Y.Z --date "DD Month YYYY"
```

This collects all fragments, updates CHANGES.md, and removes the fragment files.

## Preview

To preview what the changelog will look like:

```bash
uv run --group dev towncrier build --draft --version X.Y.Z
```
