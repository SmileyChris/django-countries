# Multiple Country Selection

## Overview

The `CountryField` can allow multiple selections of countries, which are saved as a comma-separated string. The field will always output a list of countries in this mode.

## Basic Usage

```python
from django.db import models
from django_countries.fields import CountryField

class Incident(models.Model):
    title = models.CharField(max_length=100)
    countries = CountryField(multiple=True)
```

## Working with Multiple Countries

When you access the field, it returns a list of `Country` objects:

```python
>>> incident = Incident.objects.get(title="Pavlova dispute")
>>> for country in incident.countries:
...     print(country.name)
Australia
New Zealand
```

## Data Storage Behavior

By default, countries are stored with the following behaviors:

- **Sorted**: Countries are stored in a consistent sorted order for data consistency
- **Unique**: Duplicate countries are automatically removed

### Customizing Storage Behavior

You can override these default behaviors using field arguments:

#### Disable Sorting

To store countries in the order they were added rather than sorted:

```python
countries = CountryField(multiple=True, multiple_sort=False)
```

#### Allow Duplicates

To allow duplicate country codes:

```python
countries = CountryField(multiple=True, multiple_unique=False)
```

#### Combine Both

You can combine both options:

```python
countries = CountryField(
    multiple=True,
    multiple_sort=False,
    multiple_unique=False
)
```

## Forms and Widgets

In forms, multiple country fields render as a multi-select dropdown by default. Users can select multiple countries using Ctrl/Cmd+Click or Shift+Click.

```python
from django import forms
from myapp.models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'countries']
```

### Django Admin Integration

For a better user experience in Django admin, you can use Django's `FilteredSelectMultiple` widget, which provides a dual-listbox interface similar to `filter_horizontal`:

```python
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django_countries import countries
from myapp.models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = '__all__'

    countries = forms.MultipleChoiceField(
        choices=list(countries),
        widget=FilteredSelectMultiple("Countries", is_stacked=False),
        required=False,
    )

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    form = IncidentForm
```

This provides a much more intuitive interface with search and filtering capabilities, making it easier to select from the full list of countries.

**Note:** If the field is required, set `required=True` in the `MultipleChoiceField` definition.

## Querying

You can query multiple country fields using the `__contains` lookup to match individual countries within the comma-separated list:

```python
# Find incidents involving New Zealand
>>> Incident.objects.filter(countries__contains='NZ')

# Find incidents involving Australia
>>> Incident.objects.filter(countries__name='Australia')
```

Note that `__contains` performs a substring match on the stored comma-separated codes.

### Django Admin Filtering

!!! info "New in development version"

    The `CountryFilter` in Django admin automatically works with `multiple=True` fields.

The `CountryFilter` in Django admin can be used with `multiple=True` fields:

```python
from django.contrib import admin
from django_countries.filters import CountryFilter
from myapp.models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_filter = [('countries', CountryFilter)]
```

The admin filter will:

- Show only countries that exist in your data
- Use `__contains` lookup to match countries in comma-separated lists
- Display country names in the filter dropdown for easy selection

See the [Django Admin](../usage/field.md#django-admin) section for more details, including filtering through relations.

## Example Use Cases

Multiple country selection is useful for scenarios like:

- **International incidents** spanning multiple countries
- **User profiles** where users have lived in multiple countries
- **Product availability** across multiple markets
- **Travel itineraries** visiting multiple destinations
- **Business operations** in multiple regions

## See Also

- [CountryField Reference](../usage/field.md) - Learn about single country fields
- [Forms & Widgets](../usage/forms.md) - Customize form rendering
- [Querying](../usage/field.md#querying) - Advanced query techniques
