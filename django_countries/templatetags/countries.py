from django import template
from django_countries.fields import Country


register = template.Library()


@register.assignment_tag
def get_country(code):
    return Country(code=code)
