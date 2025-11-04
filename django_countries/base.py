from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django_stubs_ext import StrPromise


try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # pragma: no cover
    # Allows this module to be executed without Django installed.
    def _(message: str) -> "StrPromise":
        return message  # type: ignore


class CountriesBase:
    COMMON_NAMES = {
        "BN": _("Brunei"),
        "BO": _("Bolivia"),
        "CD": _("Democratic Republic of the Congo"),
        "FM": _("Micronesia"),
        "GB": _("United Kingdom"),
        "GS": _("South Georgia"),
        "IR": _("Iran"),
        "KP": _("North Korea"),
        "KR": _("South Korea"),
        "LA": _("Laos"),
        "MD": _("Moldova"),
        "NL": _("Netherlands"),
        "PS": _("Palestine"),
        "RU": _("Russia"),
        "SH": _("Saint Helena"),
        "SY": _("Syria"),
        "TW": _("Taiwan"),
        "TZ": _("Tanzania"),
        "VA": _("Vatican City"),
        "VE": _("Venezuela"),
        "VN": _("Vietnam"),
    }

    OLD_NAMES = {
        "CZ": [_("Czech Republic")],
        "MK": [_("Macedonia"), _("Macedonia (the former Yugoslav Republic of)")],
        "SZ": [_("Swaziland")],
        "TZ": [_("Tanzania, the United Republic of")],
        "FK": [_("Falkland Islands  [Malvinas]")],
        "TR": [_("Turkey")],
    }

    def __getstate__(self):
        return None
