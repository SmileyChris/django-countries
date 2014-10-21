#!/usr/bin/env python
from __future__ import unicode_literals
from itertools import islice

from django_countries.conf import settings
from django.utils.encoding import force_text

try:
    import pyuca
except ImportError:
    pyuca = None

# Use UCA sorting if it's available.
if pyuca:
    collator = pyuca.Collator()
    sort_key = lambda item: collator.sort_key(item[1])
else:
    import unicodedata
    # Cheap and dirty method to sort against ASCII characters only.
    sort_key = lambda item: (
        unicodedata.normalize('NFKD', item[1])
        .encode('ascii', 'ignore').decode('ascii'))


class Countries(object):
    """
    An object containing a list of ISO3166-1 countries.

    Iterating this object will return the countries as tuples (of the country
    code and name), sorted by name.
    """

    @property
    def countries(self):
        """
        Return the a dictionary of countries, modified by any overriding
        settings.

        The result is cached so future lookups are less work intensive.
        """
        if not hasattr(self, '_countries'):
            if settings.COUNTRIES_ONLY:
                self._countries = dict(settings.COUNTRIES_ONLY)
            else:
                # Local import so that countries aren't loaded into memory
                # until first used.
                from django_countries.data import COUNTRIES, COMMON_NAMES
                self._countries = dict(COUNTRIES)
                if settings.COUNTRIES_COMMON_NAMES:
                    self._countries.update(COMMON_NAMES)
                if settings.COUNTRIES_OVERRIDE:
                    self._countries.update(settings.COUNTRIES_OVERRIDE)
                    self._countries = dict(
                        (code, name) for code, name in self._countries.items()
                        if name is not None)
        return self._countries

    @property
    def alt_codes(self):
        if not hasattr(self, '_alt_codes'):
            # Again, local import so data is not loaded unless it's needed.
            from django_countries.data import ALT_CODES
            self._alt_codes = ALT_CODES
        return self._alt_codes

    @countries.deleter
    def countries(self):
        """
        Reset the countries cache in case for some crazy reason the settings
        change. But surely no one is crazy enough to do that, right?
        """
        if hasattr(self, '_countries'):
            del self._countries

    def __iter__(self):
        """
        Return an iterator of countries, sorted by name.

        Each country record consists of a tuple of the two letter ISO3166-1
        country code and short name.

        The sorting happens based on the thread's current translation.
        """
        # Force translation before sorting.
        countries = [
            (code, force_text(name)) for code, name in self.countries.items()]

        # Return sorted country list.
        return iter(sorted(countries, key=sort_key))

    def name(self, code):
        """
        Return the name of a country, based on the code.

        If no match is found, returns an empty string.
        """
        return self.countries.get(code, '')

    def alpha3(self, code):
        """
        Return the ISO 3166-1 three letter country code matching the provided
        two letter country code.

        If no match is found, returns an empty string.
        """
        try:
            return self.alt_codes[code][0]
        except KeyError:
            return ''

    def numeric(self, code, padded=False):
        """
        Return the ISO 3166-1 numeric country code matching the provided two
        letter country code.

        If no match is found, returns ``None``.

        :param padded: Pass ``True`` to return a 0-padded three character
            string, otherwise an integer will be returned.
        """
        try:
            num = self.alt_codes[code][1]
        except KeyError:
            return None
        if padded:
            return '%03d' % num
        return num

    def __len__(self):
        """
        len() used by several third party applications to calculate the length
        of choices this will solve bug related to generating fixtures.
        """
        return len(self.countries)

    def __contains__(self, code):
        """
        Check to see if the countries contains the given code.
        """
        return code in self.countries

    def __getitem__(self, index):
        """
        Some applications expect to be able to access members of the field
        choices by index.
        """
        try:
            return next(islice(self.__iter__(), index, index+1))
        except TypeError:
            return list(islice(self.__iter__(), index.start, index.stop,
                               index.step))

countries = Countries()
