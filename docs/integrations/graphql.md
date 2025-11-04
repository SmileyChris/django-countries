# GraphQL Integration

Django Countries includes support for GraphQL through graphene-django, providing a `Country` object type for use in your GraphQL schema.

## Installation

Make sure you have graphene-django installed:

```bash
pip install graphene-django
```

## Country Object Type

A `Country` graphene object type is included that can be used when generating your schema.

### Basic Usage

```python
import graphene
from graphene_django.types import DjangoObjectType
from django_countries.graphql.types import Country
from myapp import models

class PersonType(DjangoObjectType):
    country = graphene.Field(Country)

    class Meta:
        model = models.Person
        fields = ["name", "country"]
```

## Available Fields

The `Country` object type has the following fields available:

### name

The full country name.

```graphql
{
  person {
    country {
      name
    }
  }
}
```

Response:
```json
{
  "person": {
    "country": {
      "name": "New Zealand"
    }
  }
}
```

### code

The ISO 3166-1 two character country code.

```graphql
{
  person {
    country {
      code
    }
  }
}
```

Response:
```json
{
  "person": {
    "country": {
      "code": "NZ"
    }
  }
}
```

### alpha3

The ISO 3166-1 three character country code.

```graphql
{
  person {
    country {
      alpha3
    }
  }
}
```

Response:
```json
{
  "person": {
    "country": {
      "alpha3": "NZL"
    }
  }
}
```

### numeric

The ISO 3166-1 numeric country code.

```graphql
{
  person {
    country {
      numeric
    }
  }
}
```

Response:
```json
{
  "person": {
    "country": {
      "numeric": 554
    }
  }
}
```

### iocCode

The International Olympic Committee country code.

```graphql
{
  person {
    country {
      iocCode
    }
  }
}
```

Response:
```json
{
  "person": {
    "country": {
      "iocCode": "NZL"
    }
  }
}
```

## Complete Example

Here's a complete example showing a model, object type, query, and schema:

### Model

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

### Object Types

```python
import graphene
from graphene_django import DjangoObjectType
from django_countries.graphql.types import Country
from myapp.models import Person, Company

class PersonType(DjangoObjectType):
    country = graphene.Field(Country)

    class Meta:
        model = Person
        fields = ["id", "name", "email", "country"]

class CompanyType(DjangoObjectType):
    countries = graphene.List(Country)

    class Meta:
        model = Company
        fields = ["id", "name", "countries"]
```

### Queries

```python
import graphene
from myapp.models import Person, Company
from myapp.types import PersonType, CompanyType

class Query(graphene.ObjectType):
    person = graphene.Field(PersonType, id=graphene.Int(required=True))
    people = graphene.List(PersonType)
    company = graphene.Field(CompanyType, id=graphene.Int(required=True))
    companies = graphene.List(CompanyType)

    def resolve_person(self, info, id):
        return Person.objects.get(pk=id)

    def resolve_people(self, info):
        return Person.objects.all()

    def resolve_company(self, info, id):
        return Company.objects.get(pk=id)

    def resolve_companies(self, info):
        return Company.objects.all()
```

### Schema

```python
import graphene
from myapp.queries import Query

schema = graphene.Schema(query=Query)
```

## Example Queries

### Get Person with Full Country Details

```graphql
query {
  person(id: 1) {
    name
    email
    country {
      code
      name
      alpha3
      numeric
      iocCode
    }
  }
}
```

Response:
```json
{
  "data": {
    "person": {
      "name": "Chris",
      "email": "chris@example.com",
      "country": {
        "code": "NZ",
        "name": "New Zealand",
        "alpha3": "NZL",
        "numeric": 554,
        "iocCode": "NZL"
      }
    }
  }
}
```

### Get All People with Country Names

```graphql
query {
  people {
    name
    country {
      name
    }
  }
}
```

Response:
```json
{
  "data": {
    "people": [
      {
        "name": "Chris",
        "country": {
          "name": "New Zealand"
        }
      },
      {
        "name": "Jane",
        "country": {
          "name": "Australia"
        }
      }
    ]
  }
}
```

### Get Company with Multiple Countries

```graphql
query {
  company(id: 1) {
    name
    countries {
      code
      name
    }
  }
}
```

Response:
```json
{
  "data": {
    "company": {
      "name": "Global Corp",
      "countries": [
        {
          "code": "US",
          "name": "United States"
        },
        {
          "code": "GB",
          "name": "United Kingdom"
        },
        {
          "code": "AU",
          "name": "Australia"
        }
      ]
    }
  }
}
```

## Mutations

You can also use countries in mutations:

```python
import graphene
from myapp.models import Person
from myapp.types import PersonType

class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        country_code = graphene.String(required=True)

    person = graphene.Field(PersonType)

    def mutate(self, info, name, email, country_code):
        person = Person.objects.create(
            name=name,
            email=email,
            country=country_code
        )
        return CreatePerson(person=person)

class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
```

Example mutation:

```graphql
mutation {
  createPerson(name: "John", email: "john@example.com", countryCode: "US") {
    person {
      id
      name
      country {
        code
        name
      }
    }
  }
}
```

## See Also

- [CountryField Reference](../usage/field.md) - Learn about the country field
- [Multiple Countries](../advanced/multiple.md) - Handle multiple country selection
- [Django REST Framework](drf.md) - DRF integration
