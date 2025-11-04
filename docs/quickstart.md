# Quick Start Guide

This guide will help you get started with django-countries in just a few minutes.

## Basic Usage

### Define a Model

Create a model with a `CountryField`:

```python
from django.db import models
from django_countries.fields import CountryField

class Person(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()
```

### Use in Your Code

```python
>>> from myapp.models import Person
>>> person = Person.objects.create(name="Chris", country="NZ")
>>> person.country
Country(code='NZ')
>>> person.country.name
'New Zealand'
>>> person.country.code
'NZ'
>>> person.country.flag
'/static/flags/nz.gif'
```

### Query by Country

```python
# Get all people from New Zealand
>>> Person.objects.filter(country='NZ')

# Query by country name
>>> Person.objects.filter(country__name='New Zealand')
```

## Forms

django-countries automatically provides a form field with a dropdown of all countries:

```python
from django import forms
from myapp.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'country']
```

The country field will render as a select dropdown with all countries.

## Templates

Access country properties in templates:

```django
<p>{{ person.name }} is from {{ person.country.name }}</p>
<img src="{{ person.country.flag }}" alt="{{ person.country.name }} flag">
```

### Unicode Flag Emoji

```django
<p>{{ person.country.unicode_flag }} {{ person.country.name }}</p>
```

## Admin

The country field works out of the box in Django admin with a searchable dropdown.

!!! note "Django Admin Limitations"
    `CountryField` does not currently support Django's `autocomplete_fields` feature. If you need autocomplete functionality, you'll need to use a custom form with a different widget.

    The field may also not work correctly with third-party admin filter packages like `more_admin_filters` that expect specific field types.

## Next Steps

- [CountryField Details](usage/field.md) - Learn about all field options
- [Forms & Widgets](usage/forms.md) - Customize form rendering
- [Settings](usage/settings.md) - Configure country lists and behavior
- [Template Tags](usage/templates.md) - Use template tags for advanced features
