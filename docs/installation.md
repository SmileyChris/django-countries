# Installation

## Basic Installation

Install django-countries using pip:

```bash
pip install django-countries
```

## Optional: Better Unicode Sorting

For more accurate sorting of translated country names, install with the optional [pyuca](https://pypi.python.org/pypi/pyuca/) package:

```bash
pip install django-countries[pyuca]
```

This improves sorting for non-ASCII country names by using the Unicode Collation Algorithm.

## Django Configuration

Add `django_countries` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_countries',
    # ...
]
```

## Verify Installation

You can verify the installation by running:

```python
>>> from django_countries import countries
>>> countries['NZ']
'New Zealand'
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Get up and running quickly
- [CountryField Usage](usage/field.md) - Learn about the country field
- [Settings](usage/settings.md) - Configure django-countries for your needs
