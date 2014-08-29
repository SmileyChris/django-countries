from itertools import islice
from operator import itemgetter

from django_countries.conf import settings
from django.utils.encoding import force_text


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
        return iter(sorted(countries, key=itemgetter(1)))

    def name(self, code):
        """
        Return the name of a country, based on the code.

        If no match is found, returns an empty string.
        """
        return self.countries.get(code, '')

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
