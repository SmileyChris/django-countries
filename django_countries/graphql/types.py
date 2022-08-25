from typing import Any, Optional

import graphene  # type: ignore [import]

from django_countries.fields import Country as RealCountry


class Country(graphene.ObjectType):  # type: ignore [misc]
    name = graphene.String(description="Country name")
    code = graphene.String(description="ISO 3166-1 two character country code")
    alpha3 = graphene.String(description="ISO 3166-1 three character country code")
    numeric = graphene.Int(description="ISO 3166-1 numeric country code")
    ioc_code = graphene.String(
        description="International Olympic Committee country code"
    )

    @staticmethod
    def resolve_name(country: RealCountry, info: Any) -> str:
        return country.name

    @staticmethod
    def resolve_code(country: RealCountry, info: Any) -> str:
        return country.code

    @staticmethod
    def resolve_alpha3(country: RealCountry, info: Any) -> str:
        return country.alpha3

    @staticmethod
    def resolve_numeric(country: RealCountry, info: Any) -> Optional[int]:
        return country.numeric

    @staticmethod
    def resolve_ioc_code(country: RealCountry, info: Any) -> str:
        return country.ioc_code
