from django import VERSION, template
from django_countries.fields import Country


register = template.Library()

simple_tag = register.assignment_tag if VERSION < (1, 9) else register.simple_tag

@simple_tag
def get_country(code):
    return Country(code=code)
