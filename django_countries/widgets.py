from django.forms import widgets
from django.utils.html import escape

from django_countries.conf import settings

COUNTRY_CHANGE_HANDLER = (
    "this.nextSibling.src = '%s'"
    ".replace('{code}', this.value.toLowerCase() || '__')"
    ".replace('{code_upper}', this.value.toUpperCase() || '__');"
)

FLAG_IMAGE = (
    '<img style="margin: 6px 4px; position: absolute;" src="{0}">')


class CountrySelectWidget(widgets.Select):

    def render(self, name, value, attrs=None):
        from django_countries.fields import Country
        attrs = attrs or {}
        attrs['onchange'] = (
            COUNTRY_CHANGE_HANDLER % settings.COUNTRIES_FLAG_URL)
        data = super(CountrySelectWidget, self).render(name, value, attrs)
        country = Country(value or '__')
        data += FLAG_IMAGE.format(escape(country.flag))
        return data
