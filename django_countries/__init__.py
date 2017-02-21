#!/usr/bin/env python
from __future__ import unicode_literals
from itertools import islice

from django_countries.conf import settings
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import override

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
    def get_option(self, option):
        """
        Get a configuration option, trying the options attribute first and
        falling back to a Django project setting.
        """
        value = getattr(self, option, None)
        if value is not None:
            return value
        return getattr(settings, 'COUNTRIES_{0}'.format(option.upper()))

    @property
    def countries(self):
        """
        Return the a dictionary of countries, modified by any overriding
        options.

        The result is cached so future lookups are less work intensive.
        """
        if not hasattr(self, '_countries'):
            only = self.get_option('only')
            if only:
                only_choices = True
                if not isinstance(only, dict):
                    for item in only:
                        if isinstance(item, six.string_types):
                            only_choices = False
                            break
            if only and only_choices:
                self._countries = dict(only)
            else:
                # Local import so that countries aren't loaded into memory
                # until first used.
                from django_countries.data import COUNTRIES, COMMON_NAMES
                self._countries = dict(COUNTRIES)
                if self.get_option('common_names'):
                    self._countries.update(COMMON_NAMES)
                override = self.get_option('override')
                if override:
                    self._countries.update(override)
                    self._countries = dict(
                        (code, name) for code, name in self._countries.items()
                        if name is not None)
            if only and not only_choices:
                countries = {}
                for item in only:
                    if isinstance(item, six.string_types):
                        countries[item] = self._countries[item]
                    else:
                        key, value = item
                        countries[key] = value
                self._countries = countries
            region_only = set(self.get_option('region_only') or [])
            if region_only and isinstance(self.regions, Regions):
                countries = {}
                for country in self._countries:
                    country_regions = self.parent_regions(country)
                    if region_only.intersection(country_regions):
                        countries[country] = self._countries[country]
                self._countries = countries
            self.countries_first = []
            first = self.get_option('first') or []
            for code in first:
                code = self.alpha2(code)
                if code in self._countries:
                    self.countries_first.append(code)
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
        Reset the countries cache in case for some crazy reason the settings or
        internal options change. But surely no one is crazy enough to do that,
        right?
        """
        if hasattr(self, '_countries'):
            del self._countries

    def __iter__(self):
        """
        Iterate through countries, sorted by name.

        Each country record consists of a tuple of the two letter ISO3166-1
        country code and short name.

        The sorting happens based on the thread's current translation.

        Countries that are in ``settings.COUNTRIES_FIRST`` will be displayed
        before any sorted countries (in the order provided), and are only
        repeated in the sorted list if ``settings.COUNTRIES_FIRST_REPEAT`` is
        ``True``.

        The first countries can be separated from the sorted list by the value
        provided in ``settings.COUNTRIES_FIRST_BREAK``.
        """
        # Initializes countries_first, so needs to happen first.
        countries = self.countries

        # Yield countries that should be displayed first.
        countries_first = (
            (code, force_text(countries[code]))
            for code in self.countries_first
        )

        if self.get_option('first_sort'):
            countries_first = sorted(countries_first, key=sort_key)

        for item in countries_first:
            yield item

        if self.countries_first:
            first_break = self.get_option('first_break')
            if first_break:
                yield ('', force_text(first_break))

        # Force translation before sorting.
        first_repeat = self.get_option('first_repeat')
        countries = (
            (code, force_text(name)) for code, name in countries.items()
            if first_repeat or code not in self.countries_first)

        # Return sorted country list.
        for item in sorted(countries, key=sort_key):
            yield item

    def alpha2(self, code):
        """
        Return the two letter country code when passed any type of ISO 3166-1
        country code.

        If no match is found, returns an empty string.
        """
        code = force_text(code).upper()
        if code.isdigit():
            lookup_code = int(code)
            find = lambda alt_codes: alt_codes[1] == lookup_code
        elif len(code) == 3:
            lookup_code = code
            find = lambda alt_codes: alt_codes[0] == lookup_code
        else:
            find = None
        if find:
            code = None
            for alpha2, alt_codes in self.alt_codes.items():
                if find(alt_codes):
                    code = alpha2
                    break
        if code in self.countries:
            return code
        return ''

    def name(self, code):
        """
        Return the name of a country, based on the code.

        If no match is found, returns an empty string.
        """
        code = self.alpha2(code)
        return self.countries.get(code, '')

    def by_name(self, country, language='en'):
        """
        Fetch a country's ISO3166-1 two letter country code from its name.

        An optional language parameter is also available.
        Warning: This depends on the quality of the available translations.

        If no match is found, returns an empty string.
        """
        with override(language):
            for code, name in self:
                if name == country:
                    return code
        return ''

    def alpha3(self, code):
        """
        Return the ISO 3166-1 three letter country code matching the provided
        country code.

        If no match is found, returns an empty string.
        """
        code = self.alpha2(code)
        try:
            return self.alt_codes[code][0]
        except KeyError:
            return ''

    def numeric(self, code, padded=False):
        """
        Return the ISO 3166-1 numeric country code matching the provided
        country code.

        If no match is found, returns ``None``.

        :param padded: Pass ``True`` to return a 0-padded three character
            string, otherwise an integer will be returned.
        """
        code = self.alpha2(code)
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
        of choices. This will solve a bug related to generating fixtures.
        """
        count = len(self.countries)
        # Add first countries, and the break if necessary.
        count += len(self.countries_first)
        if self.countries_first and self.get_option('first_break'):
            count += 1
        return count

    def __bool__(self):
        return bool(self.countries)

    __nonzero__ = __bool__

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

    @property
    def regions(self):
        if "_regions" in dir(self):
            v = getattr(self, "_regions")
            if isinstance(v, Regions):
                return v
        if "regions" in dir(self.__class__):
            v = getattr(self.__class__, "regions")
            if isinstance(v, Regions):
                return v
        if self.get_option("use_regions"):
            self.__class__.regions = Regions()
            return self.__class__.regions
        return None
    
    @regions.setter
    def regions(self, value):
        self._values = value

    def region(self, code, parent=None):
        """
        Return the region code matching the provided
        ISO 3166-1 country code.

        Returns None if no match is found,

        :param parent: Pass a region code to match regions
            up to the passed region code
        """
        if self.regions is None: return None
        code = self.numeric(code)
        if parent is not None:
            parents = self.parent_regions(code, parent)
            return parents.pop()  if len(parents) else None
        return self.regions.parent(code)

    def region_name(self, code, parent = None):
        """
        Return the region name matching the provided
        ISO 3166-1 country code.

        If no match is found, an empty string is returned

        :param parent: Pass a region code to match regions
            up to the passed region code
        """
        if self.regions is None: return ""
        code = self.region(code, parent)
        return self.regions.name(code) or ""

    def parent_regions(self, code = None, parent = None):
        """
        Return a list of region codes the provided ISO 3166-1
        country code is located in.

        Returns an empty list if no match is found

        :param upto: Pass a region code to match regions
            up to the passed region code
        """
        if self.regions is None: return []
        code = self.numeric(code)
        return self.regions.parents(code, parent)

    def in_region(self, code, region_code):
        """
        Returns True if the ISO 3166-1 country code is located within
        the provided region code
        """
        if self.regions is None: return False
        code = self.numeric(code)
        return self.regions.is_subdivision_of(code, region_code)

class Regions(object):
    """
    An object containing a list of UN M.49 regions.

    Iterating this object will return the regions as tuples (of the region
    code and name), sorted by name.
    """
    def get_option(self, option):
        """
        Get a configuration option, trying the options attribute first and
        falling back to a Django project setting.
        """
        value = getattr(self, option, None)
        if value is not None:
            return value
        return getattr(settings, 'REGIONS_{0}'.format(option.upper()))

    @property
    def regions(self):
        """
        Return a dictionary of regions, modified by any overriding
        options.
        The result is cached so future lookups are less work intensive.
        """
        if not hasattr(self, '_regions'):
            only = self.get_option('only')
            if only:
                only_choices = True
                if not isinstance(only, dict):
                    for item in only:
                        if isinstance(item, six.string_types):
                            only_choices = False
                            break
            if only and only_choices:
                self._regions = dict(only)
            else:
                from django_countries.region_data import REGIONS
                self._regions = dict(REGIONS)
                override = self.get_option('override')
                if override:
                    self._regions.update(override)
                    self._regions = dict(
                        (code, name) for code, name in self._regions.items()
                        if name is not None)
        return self._regions

    @property
    def region_map(self):
        """
        Return a dictionary of the region_map, modified by any overriding
        options.
        The result is cached so future lookups are less work intensive.
        """
        if not hasattr(self, '_region_map'):
            only = self.get_option('map_only')
            if only and not self.get_option('map_only_lookup'):
                self._region_map = only
            else:
                # Local import so that the region_map aren't loaded into memory
                # until first used.
                from django_countries.region_data import REGION_MAP
                self._region_map = dict(REGION_MAP)
                if only:
                    regions_map = {}
                    for region in only:
                        map = []
                        exclude = []
                        for code in only[region]:
                            if isinstance(code, six.string_types) and code[0] == "!":
                                codes = self.subdivisions(int(code[1:]), True)
                                if codes:
                                    exclude+= codes
                                else:
                                    exclude.append(int(code[1:]))
                            else:
                                codes = self.subdivisions(code, True)
                                if codes:
                                    map+= codes
                                else:
                                    map.append(code)
                        if exclude:
                            map = list(set(map) - set(exclude))
                        regions_map[region] = map
                    self._region_map = regions_map
        return self._region_map

    @regions.deleter
    def regions(self):
        """
        Reset the regions and map cache in case for some crazy reason the settings or
        internal options change. But surely no one is crazy enough to do that,
        right?
        """
        if hasattr(self, '_regions'):
            del self._regions
        if hasattr(self, '_region_map'):
            del self._region_map

    def __iter__(self):
        """
        Iterate through regions, sorted by name.

        Each region record consists of a tuple of the region code and name

        The sorting happens based on the thread's current translation.
        """
        # Return sorted region list.
        for item in sorted(self.regions, key=sort_key):
            yield item

    def __len__(self):
        """
        len() used by several third party applications to calculate the length
        of choices. This will solve a bug related to generating fixtures.
        """
        count = len(self.regions)
        return count

    def __bool__(self):
        return bool(self.regions)

    __nonzero__ = __bool__

    def __contains__(self, code):
        """
        Check to see if the regions contains the given code.
        """
        return code in self.regions

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

    def name(self, code):
        """
        Return the name of a region, based on the code.

        If no match is found, returns an empty string.
        """
        return self.regions.get(code, '')

    def parent(self, code):
        """
        Return the region code the provided
        region code is a subdivision of

        Returns None if no match is found,
        """
        for region_code in self.region_map:
            if code in self.region_map[region_code]:
                return region_code
        return None

    def parents(self, code, upto = None):
        """
        Return a list of region codes the provided region code
        is located in.

        Returns an empty list if no match is found

        :param upto: Pass a region code to match regions
            up to the passed region code
        """
        regions = []
        code = self.parent(code)
        while code is not None:
            regions.append(code)
            code = self.parent(code)
            if code == upto:
                break
        return regions

    def is_subdivision_of(self, code, region_code):
        """
        Returns True if the subdivion region code is located within
        the provided region code
        """
        code = self.parent(code)
        while code is not None and code != region_code:
            code = self.parent(code)
        return code == region_code

    def subdivisions(self, code, countries_only=False):
        """
        Returns a list of all region codes that are located
        within the provided region code

        :param countries_only: Pass ``True`` to only return
            regions that are countries
        """
        region_codes = []
        if code in self.region_map:
            for region_code in self.region_map[code]:
                if code != region_code:
                    region_codes+= self.subdivisions(region_code, countries_only)
                if not countries_only or region_code not in self.region_map:
                    region_codes.append(region_code);
        return region_codes

countries = Countries()