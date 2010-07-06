#!/usr/bin/env python
"""
This module can be used to regenerate the ``django_countries.countries``
module.

To regenerate that module to contain the latest list of ISO 3166-1 countries,
either call this module directly from the command line
(``python regenenerate.py``), or call the ``regenerate`` method.

"""

import os
import re
import string
import urllib2
from titlecase import titlecase

TEMPLATE = u'''from django.utils.translation import ugettext_lazy as _

# Nicely titled (and translatable) country names.
COUNTRIES = (
%(countries)s
)

# Nicely titled country names with duplicates for those which contain a comma
# (containing the non-comma'd version).
COUNTRIES_PLUS = (
%(countries_plus)s
)

# Official capitalized country names.
OFFICIAL_COUNTRIES = {
%(official_countries)s
}
'''
OFFICIAL_COUNTRIES_LINE = u'    %(code)r: %(name)r,'
COUNTRIES_LINE = u'    (%(code)r, _(%(name)r)),'
RE_VALID_LINE = re.compile(r'\s*(?P<name>.+);(?P<code>[A-Z]{2})\s*$')
RE_ACRONYM = re.compile(r'\b[A-Z](\.[A-Za-z])+\b')
RE_MC = re.compile(r'\b(Mc)(\w)')

def _cmp_value(value):
    """
    Ensure the countries are sorted correctly by replacing unicode characters
    with the basic English letter equivalent.

    """
    value = value.replace(u'\xe9', 'e').replace(u'\xf4', 'o')
    if value.startswith(u'\xc5'):
        value = 'A%s' % value[1:]
    return value


def regenerate(location='http://www.iso.org/iso/list-en1-semic-3.txt',
               filename=None, default_encoding='ISO-8859-1'):
    """
    Generate the countries Python module from a semicolon delimited file.
    
    """
    # Get the country list.
    data = urllib2.urlopen(location)
    official_countries = []
    if ('content-type' in data.headers and
                'charset=' in data.headers['content-type']):
        encoding = data.headers['content-type'].split('charset=')[-1]
    else:
        encoding = default_encoding
    for line in data:
        match = RE_VALID_LINE.match(unicode(line, encoding))
        if not match:
            continue
        country = match.groupdict()
        official_countries.append((str(country['code']), country['name']))

    # Generate template output (and the nicely titled country names).
    official_countries_lines = []
    countries_lines = []
    countries_plus = []
    for code, name in official_countries:
        country_data = {'code': code, 'name': name}
        official_countries_lines.append(OFFICIAL_COUNTRIES_LINE % country_data)
        name = string.capwords(name)
        name = RE_ACRONYM.sub(lambda match: match.group().upper(), name)
        if ', ' in name:
            important, rest = name.split(', ', 1)
            important = titlecase(important)
            # Temporarily add on a space so titlecase doesn't think that ending
            # shortwords should be titled.
            rest = titlecase('%s ' % rest)[:-1]
            plus_name = '%s %s' % (rest, important)
            plus_name = RE_MC.sub(lambda match: '%s%s' %
                                     (match.group(1), match.group(2).upper()),
                                  plus_name)
            countries_plus.append((plus_name, code))
            name = '%s, %s' % (important, rest)
        else:
            name = titlecase(name)
        name = RE_MC.sub(lambda match: '%s%s' % (match.group(1),
                                                 match.group(2).upper()), name)
        country_data['name'] = name
        countries_lines.append(COUNTRIES_LINE % country_data)
        countries_plus.append((name, code))
    # Order the countries_plus list of countries.
    countries_plus.sort(cmp=lambda a, b: cmp((_cmp_value(a[0]), a[1]),
                                             (_cmp_value(b[0]), b[1])))
    countries_plus_lines = []
    for name, code in countries_plus:
        country_data = {'code': code, 'name': name}
        countries_plus_lines.append(COUNTRIES_LINE % country_data)

    # Generate and save the file.
    if not filename:
        filename = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))), 'countries.py')
    # TODO: first make a backup of the file if it exists already.
    f = open(filename, 'w')
    f.write(TEMPLATE % {
        'official_countries': '\n'.join(official_countries_lines),
        'countries': '\n'.join(countries_lines),
        'countries_plus': '\n'.join(countries_plus_lines)
    })
    f.close()


if __name__ == '__main__':
    # TODO: use parseopt for location / filename
    regenerate()
