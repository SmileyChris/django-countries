### Features Added

- **Rich Country Metadata**: Added metadata properties to the `Country` object.
    - **Included Fields**: `currency_name`, `currency_symbol`, `calling_code`, `utc_offset`, `capital_city`, `continent`, `date_format`, `official_language`, and `timezones`.
    - **Reason**: To allow developers to access essential country information directly from the `Country` instance (e.g., `country.currency_symbol`) without relying on external libraries or complex lookups. This streamlines internationalization and data display logic.

- **Optimized Data Storage**: Metadata is sourced from a local, optimized YAML file (`country_metadata.yaml`) and cached in memory.
    - **Reason**: To ensure high performance and low latency when accessing country data, avoiding the overhead of repetitive file reads or database queries.

- **Enhanced Serialization**: Updated `CountryField` in Django Rest Framework serializers to include this rich metadata.
    - **Reason**: To simplify frontend integration by providing country context in a single API response, reducing the need for separate reference data endpoints.

### Usage Example

```python
from django_countries.fields import Country

# Instantiate a country object (e.g., New Zealand)
nz = Country('NZ')

# Access rich metadata properties directly
print(f"Currency: {nz.currency_name} ({nz.currency_symbol})")
print(f"Capital: {nz.capital_city}")
print(f"Calling Code: {nz.calling_code}")
print(f"Languages: {', '.join(nz.official_language)}")

# Or accessing from a model instance
class Person(models.Model):
    country = CountryField()

person = Person.objects.get(name='Alice')
person.country.currency_name
person.country.currency_symbol
person.country.calling_code
person.country.utc_offset
person.country.capital_city
person.country.continent
person.country.date_format
person.country.official_language
person.country.timezones

```

### Sample Output

Here is the data available for the `Country('NZ')` object:

| Property | Value | Description |
| :--- | :--- | :--- |
| `currency_name` | `'New Zealand dollar'` | Full name of the currency. |
| `currency_symbol` | `'$'` | Currency symbol. |
| `calling_code` | `'+64'` | International dialing code. |
| `utc_offset` | `'-11:00'` | Primary UTC offset. |
| `capital_city` | `'Wellington'` | Capital city name. |
| `continent` | `'Oceania'` | Continent the country belongs to. |
| `date_format` | `'DD/MM/YYYY'` | Common date format used. |
| `official_language` | `['English', 'Māori', 'New Zealand Sign Language']` | List of official languages. |
| `timezones` | `['UTC−11:00', 'UTC−10:00', 'UTC+12:00', 'UTC+12:45', 'UTC+13:00']` | All timezones observed. |
