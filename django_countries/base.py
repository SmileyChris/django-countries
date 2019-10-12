try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    def _(x):
        return x


class CountriesBase(object):
    COMMON_NAMES = {
        "BN": _("Brunei"),
        "BO": _("Bolivia"),
        "GB": _("United Kingdom"),
        "IR": _("Iran"),
        "KP": _("North Korea"),
        "KR": _("South Korea"),
        "LA": _("Laos"),
        "MD": _("Moldova"),
        "RU": _("Russia"),
        "SY": _("Syria"),
        "TW": _("Taiwan"),
        "TZ": _("Tanzania"),
        "VE": _("Venezuela"),
        "VN": _("Vietnam"),
    }

    OLD_NAMES = {
        "CZ": [_("Czech Republic")],
        "MK": [_("Macedonia"), _("Macedonia (the former Yugoslav Republic of)")],
        "SZ": [_("Swaziland")],
        "TZ": [_("Tanzania, the United Republic of")],
    }

    def __getstate__(self):
        return None
