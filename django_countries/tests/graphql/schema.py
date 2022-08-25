import graphene  # type: ignore [import]
import graphene_django  # type: ignore [import]
from django_countries.fields import Country
from django_countries.graphql.types import Country as CountryType
from django_countries.tests import models


class Person(graphene_django.DjangoObjectType):  # type: ignore [misc]
    country = graphene.Field(CountryType)

    class Meta:
        model = models.Person
        fields = ["name", "country"]


class Query(graphene.ObjectType):  # type: ignore [misc]
    new_zealand = graphene.Field(CountryType)
    people = graphene.List(Person)

    @staticmethod
    def resolve_new_zealand(parent, info):
        return Country(code="NZ")

    @staticmethod
    def resolve_people(parent, info):
        return models.Person.objects.all()


schema = graphene.Schema(query=Query)
