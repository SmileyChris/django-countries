import graphene  # type: ignore
import graphene_django  # type: ignore

from django_countries.fields import Country
from django_countries.graphql.types import Country as CountryType
from django_countries.tests import models


class Person(graphene_django.DjangoObjectType):
    country = graphene.Field(CountryType)

    class Meta:
        model = models.Person
        fields = ["name", "country"]


class AllowNullType(graphene_django.DjangoObjectType):
    country = graphene.Field(CountryType)

    class Meta:
        model = models.AllowNull
        fields = ["id", "country"]


class Query(graphene.ObjectType):
    new_zealand = graphene.Field(CountryType)
    people = graphene.List(Person)
    allow_nulls = graphene.List(AllowNullType)

    @staticmethod
    def resolve_new_zealand(parent, info):
        return Country(code="NZ")

    @staticmethod
    def resolve_people(parent, info):
        return models.Person.objects.all()

    @staticmethod
    def resolve_allow_nulls(parent, info):
        return models.AllowNull.objects.all()


schema = graphene.Schema(query=Query)
