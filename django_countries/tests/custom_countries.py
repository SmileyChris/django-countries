from django.utils.translation import gettext_lazy as _
from django_countries import Countries


class FantasyCountries(Countries):
    only = ["NZ", ("NV", "Neverland")]


class GBRegionCountries(Countries):
    override = {
        "GB": None,
        "GB-ENG": _("England"),
        "GB-NIR": _("Northern Ireland"),
        "GB-SCT": _("Scotland"),
        "GB-WLS": _("Wales"),
    }
