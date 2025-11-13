# Django REST Framework Integration

Django Countries provides full integration with Django REST Framework (DRF) for serializing country fields.

## CountryFieldMixin

The `CountryFieldMixin` makes the `CountryField` model field compatible with DRF serializers. Use this mixin with your model serializer:

```python
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from myapp import models

class PersonSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ("name", "email", "country")
```

This mixin handles both standard and [multi-choice](../advanced/multiple.md) country fields automatically.

## CountryField Serializer Field

For lower level use (or when not dealing with model fields), you can use the included `CountryField` serializer field:

```python
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    country = CountryField()
```

### Custom Countries Instance

You can optionally instantiate the field with the `countries` argument to specify a custom `Countries` instance:

```python
from django_countries import Countries
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

class EUCountries(Countries):
    only = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
            "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
            "PL", "PT", "RO", "SK", "SI", "ES", "SE"]

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    country = CountryField(countries=EUCountries)
```

## REST Output Format

### Default: Country Code

By default, the field will output just the country code:

```python
class PersonSerializer(serializers.Serializer):
    country = CountryField()
```

```json
{
  "country": "NZ"
}
```

### Name Only

To output the full country name instead, instantiate the field with `name_only=True`:

```python
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    country = CountryField(name_only=True)
```

```json
{
  "country": "New Zealand"
}
```

### Verbose Dictionary

For more verbose output, instantiate the field with `country_dict=True`:

```python
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    country = CountryField(country_dict=True)
```

This results in the following output structure:

```json
{
  "country": {
    "code": "NZ",
    "name": "New Zealand"
  }
}
```

Instead of a boolean you can also pass an iterable (or even a single string)
to `country_dict` to control which keys are included, in the order you
specify. Supported keys are `code`, `name`, `alpha3`, `numeric`,
`unicode_flag`, and `ioc_code`.

```python
class PersonSerializer(serializers.Serializer):
    country = CountryField(country_dict=("name", "alpha3"))
```

```json
{
  "country": {
    "name": "New Zealand",
    "alpha3": "NZL"
  }
}
```

Legacy `include_*` keyword arguments have been removed in favour of this
explicit key list.

### Input Acceptance

Regardless of the `country_dict` argument's value, both the country code string and the verbose dictionary structure are acceptable as input:

```python
# Both of these are valid input
{"country": "NZ"}
{"country": {"code": "NZ", "name": "New Zealand"}}
```

Country names are also accepted and will respect Django's active language:

```python
# With LANGUAGE_CODE="fr"
{"country": "Allemagne"}  # Resolves to "DE"

# With LANGUAGE_CODE="en"
{"country": "Germany"}    # Also resolves to "DE"
```

Note: English names are always accepted as fallback, regardless of the active language.

## OPTIONS Request

When you request OPTIONS against a resource (using the DRF [metadata support](http://www.django-rest-framework.org/api-guide/metadata/)), the countries will be returned in the response as choices:

### Request

```http
OPTIONS /api/person/ HTTP/1.1
```

### Response

```http
HTTP/1.1 200 OK
Content-Type: application/json
Allow: GET, POST, HEAD, OPTIONS
```

```json
{
  "actions": {
    "POST": {
      "country": {
        "type": "choice",
        "label": "Country",
        "choices": [
          {
            "display_name": "Afghanistan",
            "value": "AF"
          },
          {
            "display_name": "Åland Islands",
            "value": "AX"
          },
          {
            "display_name": "Albania",
            "value": "AL"
          }
        ]
      }
    }
  }
}
```

This makes it easy to build dynamic forms in client applications.

## Complete Example

Here's a complete example showing a model, serializer, and viewset:

### Models

```python
from django.db import models
from django_countries.fields import CountryField

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = CountryField()

class Company(models.Model):
    name = models.CharField(max_length=200)
    countries = CountryField(multiple=True)
```

### Serializers

```python
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from myapp.models import Person, Company

class PersonSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "name", "email", "country")

class CompanySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "countries")
```

### Views

```python
from rest_framework import viewsets
from myapp.models import Person, Company
from myapp.serializers import PersonSerializer, CompanySerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
```

### URLs

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import PersonViewSet, CompanyViewSet

router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## See Also

- [CountryField Reference](../usage/field.md) - Learn about the country field
- [Multiple Countries](../advanced/multiple.md) - Handle multiple country selection
- [Customization](../advanced/customization.md) - Customize country lists
- [GraphQL Integration](graphql.md) - Use with GraphQL
