# Django Countries

<p align="center">
  <img src="https://raw.githubusercontent.com/SmileyChris/django-countries/main/docs/images/logo.png" alt="Django Countries Logo" width="164">
</p>

<p align="center">
  <a href="https://badge.fury.io/py/django-countries"><img src="https://badge.fury.io/py/django-countries.svg" alt="PyPI version"></a>
  <a href="https://github.com/SmileyChris/django-countries/actions/workflows/tests.yml"><img src="https://github.com/SmileyChris/django-countries/actions/workflows/tests.yml/badge.svg" alt="Build status"></a>
</p>

A Django application that provides country choices for use with forms, flag icons static files, and a country field for models.

## Documentation

📚 **[Read the full documentation](https://smileychris.github.io/django-countries/)**

## Quick Start

Install:
```bash
pip install django-countries
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'django_countries',
]
```

Use in your models:
```python
from django_countries.fields import CountryField

class Person(models.Model):
    country = CountryField()
```

## Features

- **Country Field**: Django model field with all ISO 3166-1 countries
- **Translated Names**: Country names translated using Django's i18n system
- **Flag Icons**: Static flag image files for all countries
- **REST Framework**: Full Django REST Framework integration
- **GraphQL**: Support for graphene-django
- **Multiple Selection**: Support for multiple country selection

## Support

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **Django**: 3.2 (LTS), 4.2 (LTS), 5.0, 5.1, 5.2
- **Django REST Framework**: 3.11+

## Contributing

Contributions are welcome! See the [Contributing Guide](https://smileychris.github.io/django-countries/contributing/) for details.

## Translations

Country names are translated using Django's standard `gettext` and imported from our [Transifex project](https://explore.transifex.com/smileychris/django-countries/).
