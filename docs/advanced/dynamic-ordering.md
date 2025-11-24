# Dynamic Country Ordering

**New in version 8.2**

Django-countries supports dynamic country ordering based on user language, preferences, or other contextual factors. This allows you to automatically show relevant countries first in dropdowns and forms.

!!! note "First countries behavior settings"
    Several settings control how "first" countries are displayed:

    - **`COUNTRIES_FIRST_REPEAT`** (default: `False`) - Whether first countries are repeated in the main alphabetical list. When `False`, France shown first won't appear again under 'F'.
    - **`COUNTRIES_FIRST_SORT`** (default: `False`) - Whether to alphabetically sort the first countries instead of using the specified order.
    - **`COUNTRIES_FIRST_BREAK`** (default: `None`) - Optional separator text between first countries and the main list (e.g., `"─────"`).

    These settings apply to all dynamic ordering methods (`COUNTRIES_FIRST_BY_LANGUAGE`, `COUNTRIES_FIRST_AUTO_DETECT`, and `countries_context()`).

## Why Dynamic Ordering?

Different users need different countries prominently displayed:

- **French users** might expect France, Belgium, Switzerland first
- **German users** might expect Germany, Austria, Switzerland first
- **French Canadian users** might expect Canada before France
- **Users with saved preferences** might have specific countries they frequently use

Static settings like `COUNTRIES_FIRST` show the same countries for all users. Dynamic ordering adapts to each user's context.

## Auto-Detection Only

The simplest form of dynamic ordering is auto-detection. This feature is **independent** from language-based ordering and **combines with** `COUNTRIES_FIRST` by prepending the auto-detected country:

```python
# settings.py
COUNTRIES_FIRST_AUTO_DETECT = True
COUNTRIES_FIRST = ['US', 'GB']
```

**Results:**
- `en-AU` user → `['AU', 'US', 'GB']` (Australia prepended to COUNTRIES_FIRST)
- `en-GB` user → `['GB', 'US']` (GB moved to front, deduplicated)
- `fr-CA` user → `['CA', 'US', 'GB']` (Canada prepended to COUNTRIES_FIRST)
- `en` user (no country code) → `['US', 'GB']` (no auto-detection, uses static)

**Without `COUNTRIES_FIRST`:**

```python
COUNTRIES_FIRST_AUTO_DETECT = True
# en-AU → ['AU'] only
# en → alphabetical
```

!!! note "Independent from language-based ordering"
    `COUNTRIES_FIRST_AUTO_DETECT` and `COUNTRIES_FIRST_BY_LANGUAGE` are independent features. `BY_LANGUAGE` determines **which** list to show (language group or `COUNTRIES_FIRST`). `AUTO_DETECT` prepends the user's country to **whichever** list was chosen.

This provides a simple solution for most use cases. If you need more control (like showing regional countries), use language-based ordering.

## Language-Based Ordering

### Basic Usage

The `COUNTRIES_FIRST_BY_LANGUAGE` setting maps language codes to country lists. When a language matches, it **completely replaces** `COUNTRIES_FIRST` (does not combine with it):

```python
# settings.py
COUNTRIES_FIRST_BY_LANGUAGE = {
    'fr': ['FR', 'CH', 'BE', 'LU'],  # Francophone countries
    'de': ['DE', 'AT', 'CH', 'LI'],  # Germanic countries
    'es': ['ES', 'MX', 'AR', 'CL'],  # Hispanic countries
}
COUNTRIES_FIRST = ['US', 'GB']  # Ignored for fr/de/es users, used for others
```

**Results:**
- `fr` user → `['FR', 'CH', 'BE', 'LU']` (language mapping, COUNTRIES_FIRST ignored)
- `de` user → `['DE', 'AT', 'CH', 'LI']` (language mapping, COUNTRIES_FIRST ignored)
- `en` user → `['US', 'GB']` (no language match, falls back to COUNTRIES_FIRST)

### Smart Locale Auto-Detection

When `COUNTRIES_FIRST_AUTO_DETECT = True`, the user's country is automatically extracted from their locale (like `fr-CA` → `CA`) and prepended to the first countries list. This works with both language-based groups and static `COUNTRIES_FIRST`.

**With language groups:**

```python
COUNTRIES_FIRST_BY_LANGUAGE = {
    'fr': ['FR', 'CH', 'BE', 'LU'],
}
COUNTRIES_FIRST_AUTO_DETECT = True

# Results for different users:
# fr       → FR, CH, BE, LU           (no country in locale)
# fr-CA    → CA, FR, CH, BE, LU       (CA auto-prepended to group)
# fr-BE    → BE, FR, CH, LU           (BE moved to front, no duplicate)
# fr-CH    → CH, FR, BE, LU           (CH moved to front)
```

**Without AUTO_DETECT enabled:**

```python
COUNTRIES_FIRST_BY_LANGUAGE = {
    'fr': ['FR', 'CH', 'BE', 'LU'],
}
# COUNTRIES_FIRST_AUTO_DETECT not set (defaults to False)

# Results:
# fr       → FR, CH, BE, LU           (base language group)
# fr-CA    → FR, CH, BE, LU           (NO auto-prepend, uses base group)
```

**With auto-detect only:**

```python
COUNTRIES_FIRST_AUTO_DETECT = True
COUNTRIES_FIRST = ['US', 'GB']

# Results:
# en-AU → AU, US, GB  (AU auto-prepended)
# en-GB → GB, US      (GB moved to front)
```

This automatic behavior means:

1. **Requires `COUNTRIES_FIRST_AUTO_DETECT = True`** to enable
2. Users see their **own country first** (extracted from locale)
3. Followed by either **related countries** from the language group OR static `COUNTRIES_FIRST`
4. No duplicate entries (existing countries move to the front)
5. Works with both `-` and `_` locale separators (`fr-CA` and `fr_CA`)

### Explicit Locale Overrides

You can override the auto-prepend behavior for specific locales:

```python
COUNTRIES_FIRST_BY_LANGUAGE = {
    'fr': ['FR', 'CH', 'BE', 'LU'],
    'fr-CA': ['CA', 'US'],           # Canadians see CA and US, not the French group
    'en': ['US', 'GB', 'AU', 'CA'],
    'en-GB': ['GB', 'IE'],           # British see GB and Ireland only
}
```

### Fallback to Static Setting

Languages not in the mapping fall back to `COUNTRIES_FIRST`:

```python
COUNTRIES_FIRST_BY_LANGUAGE = {
    'fr': ['FR', 'CH', 'BE', 'LU'],
    'de': ['DE', 'AT', 'CH', 'LI'],
}
COUNTRIES_FIRST = ['US', 'CA']  # Used for other languages
```

## Programmatic Ordering

For cases where language-based ordering isn't sufficient (user preferences, IP geolocation, A/B testing), use the `countries_context()` context manager.

### Quick Example

```python
from django_countries import countries_context

def checkout_view(request):
    # Show countries based on user's saved preferences
    if request.user.is_authenticated:
        preferred = request.user.profile.preferred_countries
    else:
        preferred = []

    with countries_context(first=preferred):
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})
```

`countries_context()` supports all country options (`first`, `only`, `first_sort`, `first_repeat`, `first_break`, `first_by_language`, `first_auto_detect`). Each option independently overrides its corresponding setting with the highest priority.

!!! info "See full documentation"
    For complete details, examples (middleware, regional restrictions, explicit overrides, etc.), and advanced usage, see the **[Temporary Context-Based Customization](customization.md#temporary-context-based-customization)** section in the Customization guide.

## Priority System

Country ordering follows this priority (highest to lowest):

1. **Thread-local context** - Set via `countries_context()` → **Each option overrides its corresponding setting**
2. **Exact locale match** - e.g., `'fr-CA'` key in `COUNTRIES_FIRST_BY_LANGUAGE` → **Overrides COUNTRIES_FIRST**
3. **Auto-detect + base language** - e.g., `fr-CA` with `AUTO_DETECT=True` → `['CA']` + `['FR', 'CH', 'BE', 'LU']` (when base language exists) → **Overrides COUNTRIES_FIRST**
4. **Base language match** - e.g., `'fr'` key in `COUNTRIES_FIRST_BY_LANGUAGE` → **Overrides COUNTRIES_FIRST**
5. **Pure auto-detect** - `COUNTRIES_FIRST_AUTO_DETECT = True` → **Prepends to COUNTRIES_FIRST**
6. **Static setting** - `COUNTRIES_FIRST` → Used as-is
7. **Alphabetical** - Default country order

**Key behaviors:**

- **`COUNTRIES_FIRST_BY_LANGUAGE`** → **Overrides** `COUNTRIES_FIRST` when language matches
- **`COUNTRIES_FIRST_AUTO_DETECT`** → **Independent** feature that prepends user's country
- **Both settings enabled** → Auto-detect prepends to whichever list was chosen (language group or `COUNTRIES_FIRST`)

**Examples of how they work together:**

```python
# Example 1: BY_LANGUAGE overrides COUNTRIES_FIRST
COUNTRIES_FIRST_BY_LANGUAGE = {'fr': ['FR', 'CH', 'BE', 'LU']}
COUNTRIES_FIRST = ['US', 'GB']

# fr user → ['FR', 'CH', 'BE', 'LU']  (BY_LANGUAGE overrides)
# en user → ['US', 'GB']              (falls back to COUNTRIES_FIRST)
```

```python
# Example 2: AUTO_DETECT prepends to the chosen list
COUNTRIES_FIRST_BY_LANGUAGE = {'fr': ['FR', 'CH', 'BE', 'LU']}
COUNTRIES_FIRST_AUTO_DETECT = True
COUNTRIES_FIRST = ['US', 'GB']

# fr user    → ['FR', 'CH', 'BE', 'LU']     (BY_LANGUAGE, no country to detect)
# fr-CA user → ['CA', 'FR', 'CH', 'BE', 'LU'] (AUTO_DETECT prepends to BY_LANGUAGE)
# en user    → ['US', 'GB']                  (COUNTRIES_FIRST, no country to detect)
# en-AU user → ['AU', 'US', 'GB']            (AUTO_DETECT prepends to COUNTRIES_FIRST)
```

This design allows you to:
- Use `BY_LANGUAGE` for specific regional groupings that completely replace defaults
- Use `AUTO_DETECT` to automatically prioritize the user's own country
- Combine both for comprehensive, user-aware country ordering

## Per-Field Customization

Different fields can have different language mappings or auto-detection:

```python
from django_countries import Countries
from django_countries.fields import CountryField

class ShippingCountries(Countries):
    """Countries we ship to, with regional grouping."""
    first_by_language = {
        'en': ['US', 'GB', 'AU', 'CA'],
        'de': ['DE', 'AT', 'CH'],
        'fr': ['FR', 'BE', 'CH', 'CA'],
    }
    only = ['US', 'GB', 'AU', 'CA', 'DE', 'AT', 'CH', 'FR', 'BE']

class SimpleAutoDetect(Countries):
    """Just auto-detect user's country, no language groups."""
    first_auto_detect = True

class Order(models.Model):
    shipping_country = CountryField(countries=ShippingCountries)
    billing_country = CountryField(countries=SimpleAutoDetect)
    origin_country = CountryField()  # Uses global settings
```

## Caching Behavior

Country lists are **cached per language and per ordering configuration**. This means:

- Changing language triggers a new cache entry
- Changing first countries (via context) triggers a new cache entry
- Within the same language and ordering, the cache is reused
- No expensive re-sorting on every iteration

The cache is thread-safe and automatically invalidates when the configuration changes.

## Real-World Examples

### E-commerce Site with Shipping Regions

```python
# settings.py
COUNTRIES_FIRST_BY_LANGUAGE = {
    'en': ['US', 'CA', 'GB', 'AU'],
    'en-GB': ['GB', 'IE'],
    'fr': ['FR', 'BE', 'CH', 'CA'],
    'de': ['DE', 'AT', 'CH'],
    'es': ['ES', 'MX', 'AR'],
}
```

### Multi-Tenant SaaS with Region Preferences

```python
# middleware.py
class TenantCountriesMiddleware:
    def __call__(self, request):
        tenant = request.tenant  # From django-tenant-schemas or similar

        # Use tenant's preferred countries
        first = tenant.settings.get('preferred_countries', [])

        with countries_context(first=first):
            response = self.get_response(request)
        return response
```

### Form with User-Specific Ordering

```python
# forms.py
from django_countries import countries_context

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        # Set ordering based on user's previous selections
        previous_countries = []
        if user and user.is_authenticated:
            # Get user's 3 most recently used countries
            previous_countries = list(
                user.orders.values_list('country', flat=True)
                .distinct()[:3]
            )

        with countries_context(first=previous_countries):
            super().__init__(*args, **kwargs)
```

## Django REST Framework Integration

Dynamic ordering works seamlessly with DRF serializers:

```python
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

class OrderSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'shipping_country', 'billing_country']
```

The serializer will use the current language and any active `countries_context()` when rendering country choices.

## Performance Considerations

- **First call cost**: The first iteration in a given language/ordering requires translation and sorting
- **Subsequent calls**: Fully cached, very fast
- **Memory**: Each language/ordering combination gets one cache entry
- **Thread safety**: Uses `asgiref.local.Local` for thread-local context

For high-traffic sites, the caching ensures minimal performance impact even with complex language-based ordering.

## See Also

- [Customization Guide](customization.md) - Complete `countries_context()` documentation and other customization patterns
- [Settings Reference](../usage/settings.md) - All configuration options
- [CountryField Reference](../usage/field.md) - Field options
