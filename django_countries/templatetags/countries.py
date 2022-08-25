from typing import List

from django import template

from django_countries import CountryTuple, countries
from django_countries.fields import Country


register = template.Library()


@register.simple_tag
def get_country(code: str) -> Country:
    return Country(code=code)


@register.simple_tag
def get_countries() -> List[CountryTuple]:
    return list(countries)
