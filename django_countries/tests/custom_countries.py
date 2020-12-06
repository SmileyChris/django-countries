from django_countries import Countries
from django.utils.translation import gettext_lazy as _


class FantasyCountries(Countries):
    only = ["NZ", ("NV", "Neverland")]


class TranslationFallbackCountries(Countries):
    COMMON_NAMES = {"YE": "YYYemen"}
    OLD_NAMES = {"NZ": [_("New Zealand")]}
