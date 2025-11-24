# Settings Reference

This page documents all available Django settings for configuring django-countries.

All settings are optional and have sensible defaults. Add them to your Django project's `settings.py` file to customize behavior.

## Country List Settings

### COUNTRIES_COMMON_NAMES

**Type:** `bool`
**Default:** `True`

Controls whether to use common/friendly country names instead of official ISO 3166-1 names.

When `True`, uses friendlier names like "Bolivia" instead of "Bolivia, Plurinational State of". See [ISO 3166-1 Country Name Formatting](../iso3166-formatting.md) for details on the official naming patterns.

```python
# Use official ISO 3166-1 names
COUNTRIES_COMMON_NAMES = False
```

### COUNTRIES_ONLY

**Type:** `list`
**Default:** `None` (all countries)

Limits the available countries to a specific list. Can be a list of country codes, tuples of `(code, name)`, or dictionaries.

```python
# Simple list of codes
COUNTRIES_ONLY = ["US", "CA", "MX"]

# With custom names
from django.utils.translation import gettext_lazy as _

COUNTRIES_ONLY = [
    "US",
    "GB",
    ("NZ", _("Middle Earth")),
    ("AU", _("Desert")),
]
```

See [Customization](../advanced/customization.md#limit-to-specific-countries) for more details.

### COUNTRIES_OVERRIDE

**Type:** `dict`
**Default:** `{}`

Override names or metadata for specific countries. Set a country to `None` to exclude it from the list.

```python
from django.utils.translation import gettext_lazy as _

COUNTRIES_OVERRIDE = {
    "NZ": _("Middle Earth"),
    "AU": None,  # Exclude Australia
    "US": {
        "names": [
            _("United States of America"),
            _("USA"),
        ],
    },
    "IND": {
        "names": [_("Indonesia")],
        "ioc_code": "INA",
        "flag_url": "flags/id.gif",  # Use id.gif instead of ind.gif
    },
}
```

You can override the following metadata for each country:

- **names** or **name**: Custom display names (translatable)
- **alpha3**: Custom ISO 3166-1 alpha-3 code
- **numeric**: Custom ISO 3166-1 numeric code
- **ioc_code**: Custom IOC (International Olympic Committee) code
- **flag_url**: Custom flag image URL (useful for custom country codes that need to reference existing flags)

!!! tip
    When specifying only metadata fields (like `flag_url`, `ioc_code`) without providing `name` or `names`, the original country name is preserved. This allows you to customize flags or codes without losing the standard country name.

See [Customization](../advanced/customization.md#override-specific-countries) for more details.

## Display Order Settings

### COUNTRIES_FIRST

**Type:** `list`
**Default:** `None`

List of country codes to show at the beginning of the country list, before the alphabetically sorted countries.

```python
# Show US, UK, and Canada first
COUNTRIES_FIRST = ["US", "GB", "CA"]
```

!!! tip "Dynamic ordering"
    For language-based or automatic country ordering, see [`COUNTRIES_FIRST_BY_LANGUAGE`](#countries_first_by_language) and [`COUNTRIES_FIRST_AUTO_DETECT`](#countries_first_auto_detect) below, or the full [Dynamic Ordering Guide](../advanced/dynamic-ordering.md).

### COUNTRIES_FIRST_SORT

**Type:** `bool`
**Default:** `False`

Whether to sort the countries specified in `COUNTRIES_FIRST` alphabetically.

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]
COUNTRIES_FIRST_SORT = True  # Will display as: CA, GB, US
```

### COUNTRIES_FIRST_REPEAT

**Type:** `bool`
**Default:** `False`

Whether to repeat the "first" countries in the main alphabetically sorted list.

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]
COUNTRIES_FIRST_REPEAT = True  # Countries appear both at top and in main list
```

### COUNTRIES_FIRST_BREAK

**Type:** `str`
**Default:** `None`

Label for an empty separator choice between "first" countries and the main list.

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]
COUNTRIES_FIRST_BREAK = "───────────"  # Adds visual separator
```

### COUNTRIES_FIRST_BY_LANGUAGE

**Type:** `dict`
**Default:** `{}`

**New in version 8.2**

Map language codes to lists of countries to show first. Enables dynamic country ordering based on the user's current language. **Overrides** `COUNTRIES_FIRST` when a language matches.

```python
COUNTRIES_FIRST_BY_LANGUAGE = {
    'fr': ['FR', 'CH', 'BE', 'LU'],      # French users
    'de': ['DE', 'AT', 'CH', 'LI'],      # German users
    'es': ['ES', 'MX', 'AR', 'CL'],      # Spanish users
}
```

**Basic behavior:**

- `fr` user → `FR, CH, BE, LU` (uses language group)
- `en` user → falls back to `COUNTRIES_FIRST` if set

**With `COUNTRIES_FIRST_AUTO_DETECT = True`:** When a user's locale includes a country code (e.g., `'fr-CA'`), that country is automatically prepended:

- `fr-CA` user → `CA, FR, CH, BE, LU` (CA auto-prepended)
- `fr-BE` user → `BE, FR, CH, LU` (BE moved to front)

!!! info "See the full guide"
    For complete details, examples, and advanced usage including the `countries_context()` API for programmatic control, see the **[Dynamic Ordering Guide](../advanced/dynamic-ordering.md)**.

### COUNTRIES_FIRST_AUTO_DETECT

**Type:** `bool`
**Default:** `False`

**New in version 8.2**

Enable automatic country detection from the user's locale. Auto-detected countries are **prepended** to `COUNTRIES_FIRST`.

```python
COUNTRIES_FIRST_AUTO_DETECT = True
COUNTRIES_FIRST = ['US', 'GB']
```

**Results:**
- `en-AU` user → `['AU', 'US', 'GB']` (AU prepended)
- `en-GB` user → `['GB', 'US']` (GB moved to front)
- `fr-CA` user → `['CA', 'US', 'GB']` (CA prepended)
- `en` user (no country) → `['US', 'GB']` (no auto-detection, uses static)

Without `COUNTRIES_FIRST`:

```python
COUNTRIES_FIRST_AUTO_DETECT = True
# en-AU user → ['AU']
# en user → alphabetical
```

!!! note
    This setting is **independent** from `COUNTRIES_FIRST_BY_LANGUAGE`. When both are enabled, auto-detection prepends the user's country to whichever list is chosen (language group or `COUNTRIES_FIRST`). See the [Dynamic Ordering Guide](../advanced/dynamic-ordering.md) for detailed examples.

## Flag Settings

### COUNTRIES_FLAG_URL

**Type:** `str`
**Default:** `"flags/{code}.gif"`

Template string for flag image URLs. Can be relative to `STATIC_URL` or an absolute URL.

Available placeholders:
- `{code}` - lowercase country code
- `{code_upper}` - uppercase country code

```python
# Use PNG flags in a subdirectory
COUNTRIES_FLAG_URL = "flags/16x10/{code_upper}.png"

# Use absolute URL
COUNTRIES_FLAG_URL = "https://cdn.example.com/flags/{code}.svg"
```

!!! note
    No validation is performed to ensure flag files exist.

## Complete Example

Here's a complete example showing multiple settings working together:

```python
from django.utils.translation import gettext_lazy as _

# Use common names
COUNTRIES_COMMON_NAMES = True

# Limit to North American countries
COUNTRIES_ONLY = ["US", "CA", "MX"]

# Show US first
COUNTRIES_FIRST = ["US"]
COUNTRIES_FIRST_BREAK = "───────────"

# Custom flag location
COUNTRIES_FLAG_URL = "images/flags/{code_upper}.png"

# Override US display
COUNTRIES_OVERRIDE = {
    "US": {
        "names": [_("United States"), _("USA")],
    },
}
```

## Per-Field Settings

Instead of project-wide settings, you can customize individual fields by creating a custom `Countries` class:

```python
from django.utils.translation import gettext_lazy as _
from django_countries import Countries
from django_countries.fields import CountryField

class EUCountries(Countries):
    only = [
        "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
        "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
        "PL", "PT", "RO", "SK", "SI", "ES", "SE",
    ]
    first = ["DE", "FR", "IT"]
    first_break = "───────────"

class Product(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(countries=EUCountries)
```

**Language-based ordering per field:**

```python
class RegionalCountries(Countries):
    first_by_language = {
        'en': ['US', 'GB', 'CA', 'AU'],
        'de': ['DE', 'AT', 'CH'],
        'fr': ['FR', 'BE', 'CH', 'CA'],
    }

class Customer(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(countries=RegionalCountries)
```

See [Single Field Customization](../advanced/customization.md#single-field-customization) for more details.

## See Also

- [Dynamic Ordering Guide](../advanced/dynamic-ordering.md) - Language-based and programmatic country ordering
- [Customization Guide](../advanced/customization.md) - Detailed customization examples
- [ISO 3166-1 Formatting](../iso3166-formatting.md) - Understanding official country name conventions
- [CountryField Reference](field.md) - Learn about the country field
- [Forms & Widgets](forms.md) - Use countries in forms
