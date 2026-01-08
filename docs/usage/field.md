# CountryField Reference

## Overview

A country field for Django models that provides all ISO 3166-1 countries as choices.

`CountryField` is based on Django's `CharField`, providing choices corresponding to the official ISO 3166-1 list of countries (with a default `max_length` of 2).

## Basic Usage

Consider the following model using a `CountryField`:

```python
from django.db import models
from django_countries.fields import CountryField

class Person(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()
```

Any `Person` instance will have a `country` attribute that you can use to get details of the person's country:

```python
>>> person = Person(name="Chris", country="NZ")
>>> person.country
Country(code='NZ')
>>> person.country.name
'New Zealand'
>>> person.country.flag
'/static/flags/nz.gif'
```

## Field Options

### blank_label

Use `blank_label` to set the label for the initial blank choice shown in forms:

```python
country = CountryField(blank_label="(select country)")
```

### Nullable Fields

!!! info "New in development version"

    Nullable `CountryField` now returns `None` instead of `Country(code=None)`.

When using `null=True` on a `CountryField`, accessing the field on a model instance returns `None` when the database value is NULL:

```python
class Person(models.Model):
    country = CountryField(null=True, blank=True)

person = Person.objects.create(country=None)
person.country  # Returns None, not Country(code=None)
```

This allows for cleaner type checking:

```python
# Check for null
if person.country is None:
    print("No country set")
else:
    print(person.country.name)

# The common boolean check still works
if person.country:
    print(person.country.name)
```

!!! warning "Breaking Change"

    Prior to this version, nullable fields returned `Country(code=None)`. Code that checked `obj.country.code is None` should now check `obj.country is None`.

## Querying

You can filter using the full English country names in addition to country codes, even though only the country codes are stored in the database by using the queryset lookups `contains`, `startswith`, `endswith`, `regex`, or their case insensitive versions. Use `__name` or `__iname` for the `exact`/`iexact` equivalent:

```python
>>> Person.objects.filter(country__name="New Zealand").count()
1
>>> Person.objects.filter(country__icontains="zealand").count()
1
```

## Django Admin

### Basic Usage

`CountryField` works out of the box in Django admin with a searchable dropdown. Simply register your model:

```python
from django.contrib import admin
from myapp.models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']  # Search by country code or name
```

The field displays correctly in `list_display`, `readonly_fields`, and forms.

### Admin Filtering

You can filter by country in Django admin using the `CountryFilter`:

```python
from django.contrib import admin
from django_countries.filters import CountryFilter

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = [('country', CountryFilter)]
```

The admin filter will:

- Show only countries that exist in your data
- Display country names in the filter dropdown for easy selection

#### Filtering Through Relations

!!! info "New in version 8.2.0"

    `CountryFilter` now supports filtering on `CountryField` through related models.

You can filter on country fields through foreign key relations:

```python
from django.contrib import admin
from django_countries.filters import CountryFilter

class Contact(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField()

class Payment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Filter payments by the country of the related contact
    list_filter = [('contact__country', CountryFilter)]
```

This works with any relation depth (e.g., `organization__contact__country`).

### Custom Admin Form with Flag Widget

To show a flag image next to the country dropdown in admin, use `CountrySelectWidget`:

```python
from django import forms
from django.contrib import admin
from django_countries.widgets import CountrySelectWidget
from myapp.models import Person

class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        widgets = {
            'country': CountrySelectWidget()
        }

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
```

The flag image will update automatically when the country selection changes.

### Limitations

!!! warning "Known Limitations"

    **Autocomplete fields**: `CountryField` does not currently support Django's `autocomplete_fields` feature. The field will fall back to a regular select widget if added to `autocomplete_fields`.

    **Third-party filters**: Some third-party admin filter packages may not work correctly with `CountryField`. Use the built-in `CountryFilter` for reliable filtering.

## The Country Object

An object used to represent a country, instantiated with a two character country code, three character code, or numeric code.

It can be compared to other objects as if it was a string containing the country code and when evaluated as text, returns the country code.

### Properties

#### name

Contains the full country name.

```python
>>> person.country.name
'New Zealand'
```

#### flag

Contains a URL to the flag. If your page could have lots of different flags then consider using `flag_css` instead to avoid excessive HTTP requests.

```python
>>> person.country.flag
'/static/flags/nz.gif'
```

#### flag_css

Output the css classes needed to display an HTML element as the correct flag from within a single sprite image that contains all flags. For example:

```django
<link rel="stylesheet" href="{% static 'flags/sprite.css' %}">
<i class="{{ country.flag_css }}"></i>
```

For multiple flag resolutions, use `sprite-hq.css` instead and add the `flag2x`, `flag3x`, or `flag4x` class. For example:

```django
<link rel="stylesheet" href="{% static 'flags/sprite-hq.css' %}">
Normal: <i class="{{ country.flag_css }}"></i>
Bigger: <i class="flag2x {{ country.flag_css }}"></i>
```

You might also want to consider using `aria-label` for better accessibility:

```django
<i class="{{ country.flag_css }}"
    aria-label="{% blocktrans with country_code=country.code %}
        {{ country_code }} flag
    {% endblocktrans %}"></i>
```

#### unicode_flag

A unicode glyph for the flag for this country. Currently well-supported in iOS and OS X. See [Regional Indicator Symbol](https://en.wikipedia.org/wiki/Regional_Indicator_Symbol) for details.

```python
>>> person.country.unicode_flag
'🇳🇿'
```

#### code

The two letter country code for this country.

```python
>>> person.country.code
'NZ'
```

#### alpha3

The three letter country code for this country.

```python
>>> person.country.alpha3
'NZL'
```

#### numeric

The numeric country code for this country (as an integer).

```python
>>> person.country.numeric
554
```

#### numeric_padded

The numeric country code as a three character 0-padded string.

```python
>>> person.country.numeric_padded
'554'
```

#### ioc_code

The three letter International Olympic Committee country code.

```python
>>> person.country.ioc_code
'NZL'
```

## Getting Countries from Python

Use the `django_countries.countries` object instance as an iterator of ISO 3166-1 country codes and names (sorted by name).

For example:

```python
>>> from django_countries import countries
>>> dict(countries)["NZ"]
'New Zealand'

>>> for code, name in list(countries)[:3]:
...     print(f"{name} ({code})")
...
Afghanistan (AF)
Åland Islands (AX)
Albania (AL)
```

## See Also

- [Multiple Countries](../advanced/multiple.md) - Select multiple countries in a single field
- [Customization](../advanced/customization.md) - Customize the country list
- [Settings](settings.md) - Configure country field behavior
