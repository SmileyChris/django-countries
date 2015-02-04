from __future__ import unicode_literals
try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse   # Python 2

from django.forms import widgets
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.functional import Promise

from django_countries.conf import settings

COUNTRY_CHANGE_HANDLER = (
    "this.nextSibling.src = '%s'"
    ".replace('{code}', this.value.toLowerCase() || '__')"
    ".replace('{code_upper}', this.value.toUpperCase() || '__');"
)

FLAG_IMAGE = (
    '{0}<img style="margin: 6px 4px; position: absolute;" src="{1}">')


class LazyChoicesMixin(object):

    @property
    def choices(self):
        """
        When it's time to get the choices, if it was a lazy then figure it out
        now and memoize the result.
        """
        if isinstance(self._choices, Promise):
            self._choices = list(self._choices)
        return self._choices

    @choices.setter
    def choices(self, value):
        self._set_choices(value)

    def _set_choices(self, value):
        self._choices = value


class LazySelect(LazyChoicesMixin, widgets.Select):
    """
    A form Select widget that respects choices being a lazy object.
    """


class CountrySelectWidget(LazySelect):

    def render(self, name, value, attrs=None):
        from django_countries.fields import Country
        attrs = attrs or {}
        attrs['onchange'] = (
            COUNTRY_CHANGE_HANDLER % urlparse.urljoin(
                settings.STATIC_URL, settings.COUNTRIES_FLAG_URL))
        data = super(CountrySelectWidget, self).render(name, value, attrs)
        if isinstance(value, Country):
            country = value
        else:
            country = Country(value or '__')
        return format_html(FLAG_IMAGE, mark_safe(data), country.flag)
