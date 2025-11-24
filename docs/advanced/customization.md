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

## Dynamic Country Ordering

For language-based ordering, automatic locale detection, and showing certain countries first, see the **[Dynamic Ordering Guide](dynamic-ordering.md)**.

Quick example of static first countries:

```python
COUNTRIES_FIRST = ["US", "GB", "CA"]  # Show these countries first
COUNTRIES_FIRST_SORT = True           # Sort them alphabetically
COUNTRIES_FIRST_REPEAT = True         # Repeat in main list
COUNTRIES_FIRST_BREAK = "───────────" # Add separator
```

The Dynamic Ordering guide covers:

- **Static ordering** - `COUNTRIES_FIRST` and related settings
- **Language-based ordering** - Show different countries first based on user's language
- **Auto-detection** - Automatically prioritize user's country from locale
- **Programmatic control** - Use `countries_context()` for per-request customization

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

## Temporary Context-Based Customization

!!! info "New in version 8.2.0"

For per-request or temporary overrides (such as in views or middleware), use the `countries_context()` context manager. This allows you to temporarily override any country option without modifying global settings or creating custom subclasses.

### Basic Usage

```python
from django_countries import countries_context

def checkout_view(request):
    # Temporarily override settings for this request
    with countries_context(first=['US', 'CA']):
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})
```

### Available Options

`countries_context()` supports all country configuration options:

- **`first`** - List of countries to show first
- **`only`** - Limit to specific countries
- **`first_sort`** - Sort first countries alphabetically
- **`first_repeat`** - Repeat first countries in main list
- **`first_break`** - Separator text between first and main list
- **`first_by_language`** - Language-based country ordering mapping
- **`first_auto_detect`** - Auto-detect country from locale

**How options work:**

Each option independently overrides its corresponding setting. For example:
- `first` overrides `COUNTRIES_FIRST`
- `first_by_language` overrides `COUNTRIES_FIRST_BY_LANGUAGE`
- `first_auto_detect` overrides `COUNTRIES_FIRST_AUTO_DETECT`

To disable a language-based mapping for a specific request, explicitly set it to an empty dict:

```python
# With COUNTRIES_FIRST_BY_LANGUAGE = {'fr': ['FR', 'CH']} in settings
with countries_context(first=['US', 'CA'], first_by_language={}):
    form = MyForm()  # Uses US, CA (not FR, CH) even for French users
```

### Common Use Cases

**User preferences:**

```python
def profile_view(request):
    if request.user.is_authenticated:
        preferred = request.user.profile.favorite_countries
    else:
        preferred = []

    with countries_context(first=preferred):
        form = ProfileForm()
    return render(request, 'profile.html', {'form': form})
```

**Regional restrictions:**

```python
def regional_signup(request):
    # Only show North American countries
    with countries_context(only=['US', 'CA', 'MX'], first=['US']):
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
```

**IP-based geolocation (via middleware):**

```python
from django_countries import countries_context
import geoip2.database

class GeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.reader = geoip2.database.Reader('/path/to/GeoLite2-Country.mmdb')

    def __call__(self, request):
        # Detect country from IP
        try:
            response = self.reader.country(request.META['REMOTE_ADDR'])
            detected_country = [response.country.iso_code]
        except Exception:
            detected_country = []

        # Apply for all forms in this request
        with countries_context(first=detected_country):
            return self.get_response(request)
```

**Sorting options:**

```python
def sorted_countries_view(request):
    # Show first countries alphabetically
    with countries_context(first=['US', 'GB', 'AU'], first_sort=True):
        form = MyForm()  # Shows: AU, GB, US (sorted)
    return render(request, 'form.html', {'form': form})
```

### Nested Contexts

Contexts can be nested, with the innermost context taking precedence:

```python
with countries_context(first=['US', 'CA']):
    form1 = MyForm()  # US, CA first

    with countries_context(first=['FR', 'DE']):
        form2 = MyForm()  # FR, DE first (overrides outer context)

    form3 = MyForm()  # Back to US, CA first
```

### Priority

Each option in `countries_context()` independently overrides its corresponding setting with the **highest priority**:

| Context Option | Overrides (in order) |
|----------------|---------------------|
| `first` | Custom `Countries.first` → `COUNTRIES_FIRST` |
| `first_by_language` | Custom `Countries.first_by_language` → `COUNTRIES_FIRST_BY_LANGUAGE` |
| `first_auto_detect` | Custom `Countries.first_auto_detect` → `COUNTRIES_FIRST_AUTO_DETECT` |
| `only` | Custom `Countries.only` → `COUNTRIES_ONLY` |
| `first_sort` | Custom `Countries.first_sort` → `COUNTRIES_FIRST_SORT` |
| `first_repeat` | Custom `Countries.first_repeat` → `COUNTRIES_FIRST_REPEAT` |
| `first_break` | Custom `Countries.first_break` → `COUNTRIES_FIRST_BREAK` |

**Important:** Options work independently. Setting `first` in the context does **not** automatically disable `COUNTRIES_FIRST_BY_LANGUAGE`. To disable language-based ordering, explicitly set `first_by_language={}`:

```python
# Language-based ordering still applies
with countries_context(first=['US']):
    pass  # French users still see FR, CH, BE, LU (from BY_LANGUAGE)

# Language-based ordering disabled
with countries_context(first=['US'], first_by_language={}):
    pass  # All users see US first
```

This explicit design makes it ideal for request-specific customization where you need precise control over which settings to override.

!!! tip "Thread-safe"
    `countries_context()` uses thread-local storage, making it safe to use in multi-threaded environments like Django views and middleware.

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

!!! info "New in version 8.2.0"

    Per-country `flag_url` overrides allow custom country codes to reuse existing flag image assets or point to bespoke flags.

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

- [Dynamic Ordering](dynamic-ordering.md) - Language-based and automatic country ordering
- [Settings Reference](../usage/settings.md) - Complete list of all settings
- [ISO 3166-1 Formatting](../iso3166-formatting.md) - Understanding official country name conventions
- [CountryField Reference](../usage/field.md) - Learn about the country field
- [Multiple Countries](multiple.md) - Handle multiple country selection
