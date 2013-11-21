from django_countries.countries import COUNTRIES
from django_countries.conf import settings


def country_list():
    """
    Return a list of countries, sorted by name.

    Each country record consists of a tuple of the short name and two letter
    ISO3166-1 country code.
    """
    country_list = []
    overrides = settings.COUNTRIES_NAME_OVERRIDES
    for code, name in COUNTRIES(name, code):
        if code in overrides:
            name = overrides['code']
        if name:
            country_list.append((name, code))
    return sorted(country_list)
