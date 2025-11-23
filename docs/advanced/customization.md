# Customization

## Customize the Country List

Country names are taken from the official ISO 3166-1 list, with some country names being replaced with their more common usage (such as "Bolivia" instead of "Bolivia, Plurinational State of"). See [ISO 3166-1 Country Name Formatting](../iso3166-formatting.md) for details on the official naming conventions and quirks.

### Use Official ISO Names

To retain the official ISO 3166-1 naming for all fields, set the `COUNTRIES_COMMON_NAMES` setting to `False`:

```python
COUNTRIES_COMMON_NAMES = False
```

### Override Specific Countries

If your project requires the use of alternative names, the inclusion or exclusion of specific countries, set the `COUNTRIES_OVERRIDE` setting to a dictionary of names which override the defaults.

!!! note
    You will need to handle translation of customized country names.

Setting a country's name to `None` will exclude it from the country list. For example:

```python
from django.utils.translation import gettext_lazy as _

COUNTRIES_OVERRIDE = {
    "NZ": _("Middle Earth"),
    "AU": None,  # Exclude Australia
    "US": {
        "names": [
            _("United States of America"),
            _("America"),
        ],
    },
}
```

### Limit to Specific Countries

If you have a specific list of countries that should be used, use `COUNTRIES_ONLY`:

```python
COUNTRIES_ONLY = ["NZ", "AU"]
```

Or to specify your own country names, use a dictionary or two-tuple list (string items will use the standard country name):

```python
from django.utils.translation import gettext_lazy as _

COUNTRIES_ONLY = [
    "US",
    "GB",
    ("NZ", _("Middle Earth")),
    ("AU", _("Desert")),
]
```

## Show Certain Countries First

Provide a list of country codes as the `COUNTRIES_FIRST` setting and they will be shown first in the countries list (in the order specified) before all the alphanumerically sorted countries:

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]
```

### Sort First Countries

If you want to sort these initial countries too, set the `COUNTRIES_FIRST_SORT` setting to `True`:

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]
COUNTRIES_FIRST_SORT = True
```

### Repeat First Countries

By default, these initial countries are not repeated again in the alphanumerically sorted list. If you would like them to be repeated, set the `COUNTRIES_FIRST_REPEAT` setting to `True`:

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]
COUNTRIES_FIRST_REPEAT = True
```

### Add Separator

You can optionally separate these "first" countries with an empty choice by providing the choice label as the `COUNTRIES_FIRST_BREAK` setting:

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]
COUNTRIES_FIRST_BREAK = "───────────"
```

## Customize the Flag URL

The `COUNTRIES_FLAG_URL` setting can be used to set the URL for the flag image assets. It defaults to:

```python
COUNTRIES_FLAG_URL = "flags/{code}.gif"
```

The URL can be relative to the `STATIC_URL` setting, or an absolute URL.

The location is parsed using Python's string formatting and is passed the following arguments:

- `code` - lowercase country code
- `code_upper` - uppercase country code

For example:

```python
COUNTRIES_FLAG_URL = "flags/16x10/{code_upper}.png"
```

!!! note
    No checking is done to ensure that a static flag actually exists.

### Per-Field Flag URL

Alternatively, you can specify a different URL on a specific `CountryField`:

```python
from django.db import models
from django_countries.fields import CountryField

class Person(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(
        countries_flag_url="//flags.example.com/{code}.png"
    )
```

## Single Field Customization

To customize an individual field rather than rely on project-level settings, create a `Countries` subclass which overrides settings.

To override a setting, give the class an attribute matching the lowercased setting without the `COUNTRIES_` prefix.

Then just reference this class in a field. For example, this `CountryField` uses a custom country list that only includes the G8 countries:

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries import Countries
from django_countries.fields import CountryField

class G8Countries(Countries):
    only = [
        "CA", "FR", "DE", "IT", "JP", "RU", "GB",
        ("EU", _("European Union"))
    ]

class Vote(models.Model):
    country = CountryField(countries=G8Countries)
    approve = models.BooleanField()
```

### Available Settings for Customization

When creating a custom `Countries` subclass, you can override these settings (without the `COUNTRIES_` prefix):

- `only` - Equivalent to `COUNTRIES_ONLY`
- `override` - Equivalent to `COUNTRIES_OVERRIDE`
- `first` - Equivalent to `COUNTRIES_FIRST`
- `first_repeat` - Equivalent to `COUNTRIES_FIRST_REPEAT`
- `first_sort` - Equivalent to `COUNTRIES_FIRST_SORT`
- `first_break` - Equivalent to `COUNTRIES_FIRST_BREAK`
- `flag_url` - Equivalent to `COUNTRIES_FLAG_URL`
- `common_names` - Equivalent to `COUNTRIES_COMMON_NAMES`

## Complex Dictionary Format

For `COUNTRIES_ONLY` and `COUNTRIES_OVERRIDE`, you can also provide a dictionary rather than just a translatable string for the country name.

The options within the dictionary are:

### name or names (required)

Either a single translatable name for this country or a list of multiple translatable names. If using multiple names, the first name takes preference when using `COUNTRIES_FIRST` or the `Country.name`.

```python
COUNTRIES_OVERRIDE = {
    "US": {
        "names": [
            _("United States of America"),
            _("USA"),
            _("America"),
        ],
    },
}
```

### alpha3 (optional)

An ISO 3166-1 three character code (or an empty string to nullify an existing code for this country):

```python
COUNTRIES_OVERRIDE = {
    "XX": {
        "names": [_("Custom Country")],
        "alpha3": "XXX",
    },
}
```

### numeric (optional)

An ISO 3166-1 numeric country code (or `None` to nullify an existing code for this country). The numeric codes 900 to 999 are left available by the standard for user-assignment:

```python
COUNTRIES_OVERRIDE = {
    "XX": {
        "names": [_("Custom Country")],
        "numeric": 900,
    },
}
```

### ioc_code (optional)

The country's International Olympic Committee code (or an empty string to nullify an existing code):

```python
COUNTRIES_OVERRIDE = {
    "XX": {
        "names": [_("Custom Country")],
        "ioc_code": "XXX",
    },
}
```

### flag_url (optional)

A custom flag image URL for this country. This is particularly useful when using custom country codes that need to reference existing flag images:

```python
COUNTRIES_OVERRIDE = {
    "ID": None,  # Remove Indonesia
    "IND": {
        "names": [_("Indonesia")],
        "ioc_code": "INA",
        "flag_url": "flags/id.gif",  # Points to id.gif instead of ind.gif
    },
}
```

The flag URL supports the same placeholders as `COUNTRIES_FLAG_URL`:

- `{code}` - lowercase country code
- `{code_upper}` - uppercase country code

!!! tip
    When specifying only metadata fields (like `flag_url`, `ioc_code`) without providing `name` or `names`, the original country name is preserved. This allows you to customize flags or codes without losing the standard country name:

    ```python
    COUNTRIES_OVERRIDE = {
        "NZ": {"flag_url": "custom/nz.png"},  # Keeps "New Zealand" name
    }
    ```

### Complete Example

```python
from django.utils.translation import gettext_lazy as _

COUNTRIES_OVERRIDE = {
    "NZ": {
        "names": [_("New Zealand"), _("Aotearoa")],
        "alpha3": "NZL",
        "numeric": 554,
        "ioc_code": "NZL",
    },
    "XX": {
        "names": [_("Custom Country")],
        "alpha3": "XXX",
        "numeric": 900,
        "ioc_code": "",
        "flag_url": "flags/custom/{code}.png",
    },
}
```

## Country Object External Plugins

Other Python packages can add attributes to the `Country` object by using entry points in their setup script.

For example, you could create a `django_countries_phone` package with the following entry point in the `setup.py` or `pyproject.toml` file. The entry point name (`phone`) will be the new attribute name on the Country object. The attribute value will be the return value of the `get_phone` function (called with the Country instance as the sole argument).

### setup.py Example

```python
setup(
    ...
    entry_points={
        "django_countries.Country": "phone = django_countries_phone.get_phone"
    },
    ...
)
```

### pyproject.toml Example

```toml
[project.entry-points."django_countries.Country"]
phone = "django_countries_phone:get_phone"
```

Then in your code:

```python
>>> from django_countries import countries
>>> country = countries['US']
>>> country.phone  # Calls get_phone(country)
'+1'
```

## See Also

- [Settings Reference](../usage/settings.md) - Complete list of all settings
- [ISO 3166-1 Formatting](../iso3166-formatting.md) - Understanding official country name conventions
- [CountryField Reference](../usage/field.md) - Learn about the country field
- [Multiple Countries](multiple.md) - Handle multiple country selection
