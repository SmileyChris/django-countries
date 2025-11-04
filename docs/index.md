# Django Countries

A Django application that provides country choices for use with forms, flag icons static files, and a country field for models.

## Features

- **Country Field**: Django model field with all ISO 3166-1 countries
- **Translated Names**: Country names translated using Django's i18n system
- **Flag Icons**: Static flag image files for all countries
- **REST Framework**: Full Django REST Framework integration
- **GraphQL**: Support for graphene-django
- **Multiple Selection**: Support for multiple country selection
- **Customizable**: Extensive settings for customization

## Quick Example

```python
from django.db import models
from django_countries.fields import CountryField

class Person(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()
```

```python
>>> from myapp.models import Person
>>> person = Person.objects.create(name="Chris", country="NZ")
>>> person.country
Country(code='NZ')
>>> person.country.name
'New Zealand'
>>> person.country.flag
'/static/flags/nz.gif'
```

## Translations

Country names are translated using Django's standard `gettext` and imported from our [Transifex project](https://explore.transifex.com/smileychris/django-countries/).

## Support

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **Django**: 3.2 (LTS), 4.2 (LTS), 5.0, 5.1
- **Django REST Framework**: 3.11+

## License

MIT License. See LICENSE file for details.

## Getting Started

Ready to use django-countries? Check out the [Installation Guide](installation.md) to get started!
