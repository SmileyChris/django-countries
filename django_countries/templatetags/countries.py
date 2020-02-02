import django
from django import template
from django_countries.fields import Country, countries


register = template.Library()
simple_tag = register.simple_tag


@simple_tag
def get_country(code):
    return Country(code=code)


@simple_tag
def get_countries():
    return list(countries)
