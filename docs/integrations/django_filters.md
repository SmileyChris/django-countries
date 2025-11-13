# Django Filters Integration

`django_countries` ships with a helper filter that plugs into
[django-filter](https://django-filter.readthedocs.io/) so you can quickly add
country filtering to list views.

## Installation

```bash
pip install django-filter
```

## Usage

```python
import django_filters
from django_countries.django_filters import CountryFilter
from .models import Person


class PersonFilterSet(django_filters.FilterSet):
    country = CountryFilter(empty_label="Any country")

    class Meta:
        model = Person
        fields = ["country"]
```

The `CountryFilter` subclass of `django_filters.ChoiceFilter` automatically
populates its `choices` from `django_countries.countries`, so you don’t need to
maintain the list yourself. You can still pass any `ChoiceFilter` arguments,
including `empty_label`, `label`, `method`, or `field_class` if you need to
customize behavior.

Use the filter set as normal—either in class-based views such as
`django_filters.views.FilterView` or manually inside a function-based view:

```python
def person_list(request):
    filterset = PersonFilterSet(request.GET, queryset=Person.objects.all())
    return render(
        request,
        "people/list.html",
        {"filter": filterset, "object_list": filterset.qs},
    )
```
