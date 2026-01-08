from graphene.test import Client  # type: ignore

from django_countries.tests.graphql.schema import schema
from django_countries.tests.models import AllowNull, Person


def test_country_type(db):
    Person.objects.create(name="Skippy", country="AU")
    client = Client(schema)
    executed = client.execute("""{ people { name, country {name} } }""")
    returned_person = executed["data"]["people"][0]
    assert returned_person == {"name": "Skippy", "country": {"name": "Australia"}}


def test_nullable_country_with_value(db):
    """Test that nullable CountryField with a value works in GraphQL."""
    AllowNull.objects.create(country="NZ")
    client = Client(schema)
    executed = client.execute("""{ allowNulls { country { code, name } } }""")
    assert "errors" not in executed, executed.get("errors")
    result = executed["data"]["allowNulls"][0]
    assert result == {"country": {"code": "NZ", "name": "New Zealand"}}


def test_nullable_country_with_null(db):
    """Test that nullable CountryField with NULL returns null in GraphQL."""
    AllowNull.objects.create(country=None)
    client = Client(schema)
    executed = client.execute("""{ allowNulls { country { code, name } } }""")
    assert "errors" not in executed, executed.get("errors")
    result = executed["data"]["allowNulls"][0]
    assert result == {"country": None}
