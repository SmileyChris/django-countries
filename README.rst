================
Django Countries
================

A Django application that provides country choices for use with forms, flag
icons static files, and a country field for models.

Installation
============

1. ``pip install django-countries``
2. Add ``django_countries`` to ``INSTALLED_APPS``

For more accurate sorting of translated country names, install the optional
pyuca_ package.

.. _pyuca: https://pypi.python.org/pypi/pyuca/


CountryField
============

A country field for Django models that provides all ISO 3166-1 countries as
choices.

``CountryField`` is based on Django's ``CharField``, providing choices
corresponding to the official ISO 3166-1 list of countries (with a default
``max_length`` of 2).

Consider the following model using a ``CountryField``::

    from django.db import models
    from django_countries.fields import CountryField

    class Person(models.Model):
        name = models.CharField(max_length=100)
        country = CountryField()

Any ``Person`` instance will have a ``country`` attribute that you can use to
get details of the person's country::

    >>> person = Person(name='Chris', country='NZ')
    >>> person.country
    Country(code='NZ')
    >>> person.country.name
    'New Zealand'
    >>> person.country.flag
    '/static/flags/nz.gif'

This object (``person.country`` in the example) is a ``Country`` instance,
which is described below.

Use ``blank_label`` to set the label for the initial blank choice shown in
forms::

    country = CountryField(blank_label='(select country)')

This field can also allow multiple selections of countries (saved as a comma
separated string). The field will always output a list of countries in this
mode. For example::

    class Incident(models.Model):
        title = models.CharField(max_length=100)
        countries = CountryField(multiple=True)

    >>> for country in Incident.objects.get(title='Pavlova dispute').countries:
    ...     print(country.name)
    Australia
    New Zealand


The ``Country`` object
----------------------

An object used to represent a country, instanciated with a two character
country code.

It can be compared to other objects as if it was a string containing the
country code and when evaluated as text, returns the country code.

name
  Contains the full country name.

flag
  Contains a URL to the flag.

unicode_flag
  A unicode glyph for the flag for this country. Currently well-supported in
  iOS and OS X. See https://en.wikipedia.org/wiki/Regional_Indicator_Symbol
  for details.

alpha3
  The three letter country code for this country.

numeric
  The numeric country code for this country (as an integer).

numeric_padded
  The numeric country code as a three character 0-padded string.

``CountrySelectWidget``
-----------------------

A widget is included that can show the flag image after the select box
(updated with JavaScript when the selection changes).

When you create your form, you can use this custom widget like normal::

    from django_countries.widgets import CountrySelectWidget

    class PersonForm(forms.ModelForm):
        class Meta:
            model = models.Person
            fields = ('name', 'country')
            widgets = {'country': CountrySelectWidget()}

Pass a ``layout`` text argument to the widget to change the positioning of the
flag and widget. The default layout is::

    '{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'


Custom forms
============

If you want to use the countries in a custom form, use the following custom
field to ensure the translatable strings for the country choices are left lazy
until the widget renders::

    from django_countries.fields import LazyTypedChoiceField

    class CustomForm(forms.Form):
        country = LazyTypedChoiceField(choices=countries)

You can also use the CountrySelectWidget_ as the widget for this field if you
want the flag image after the select box.


Get the countries from Python
=============================

Use the ``django_countries.countries`` object instance as an iterator of ISO
3166-1 country codes and names (sorted by name).

For example::

    >>> from django_countries import countries
    >>> dict(countries)['NZ']
    'New Zealand'

    >>> for code, name in list(countries)[:3]:
    ...     print("{name} ({code})".format(name=name, code=code))
    ...
    Afghanistan (AF)
    Åland Islands (AX)
    Albania (AL)

Country names are translated using Django's standard ``ugettext``.
If you would like to help by adding a translation, please visit
https://www.transifex.com/projects/p/django-countries/


Template Tags
=============

If you have your country code stored in a different place than a `CountryField`
you can use the template tag to get a `Country` object and have access to all
of its properties::

    {% load countries %}
    {% get_country 'BR' as country %}
    {{ country.name }}


Customization
=============

Customize the country list
--------------------------

Country names are taken from the official ISO 3166-1 list. If your project
requires the use of alternative names, the inclusion or exclusion of specific
countries then use the ``COUNTRIES_OVERRIDE`` setting.

A dictionary of names to override the defaults.

Note that you will need to handle translation of customised country names.

Setting a country's name to ``None`` will exclude it from the country list.
For example::

    COUNTRIES_OVERRIDE = {
        'NZ': _('Middle Earth'),
        'AU': None
    }

If you have a specific list of countries that should be used, use
``COUNTRIES_ONLY``::

    COUNTRIES_ONLY = ['NZ', 'AU']

or to specify your own country names, use a dictionary or two-tuple list
(string items will use the standard country name)::

    COUNTRIES_ONLY = [
        'US',
        'GB',
        ('NZ', _('Middle Earth')),
        ('AU', _('Desert')),
    ]


Show certain countries first
----------------------------

Provide a list of country codes as the ``COUNTRIES_FIRST`` setting and they
will be shown first in the countries list (in the order specified) before all
the alphanumerically sorted countries.

If you want to sort these initial countries too, set the
``COUNTRIES_FIRST_SORT`` setting to ``True``.

By default, these initial countries are not repeated again in the
alphanumerically sorted list. If you would like them to be repeated, set the
``COUNTRIES_FIRST_REPEAT`` setting to ``True``.

Finally, you can optionally separate these 'first' countries with an empty
choice by providing the choice label as the ``COUNTRIES_FIRST_BREAK`` setting.


Customize the flag URL
----------------------

The ``COUNTRIES_FLAG_URL`` setting can be used to set the url for the flag
image assets. It defaults to::

    COUNTRIES_FLAG_URL = 'flags/{code}.gif'

The URL can be relative to the STATIC_URL setting, or an absolute URL.

The location is parsed using Python's string formatting and is passed the
following arguments:

    * code
    * code_upper

For example: ``COUNTRIES_FLAG_URL = 'flags/16x10/{code_upper}.png'``

No checking is done to ensure that a static flag actually exists.

Alternatively, you can specify a different URL on a specific ``CountryField``::

    class Person(models.Model):
        name = models.CharField(max_length=100)
        country = CountryField(
            countries_flag_url='//flags.example.com/{code}.png')


Single field customization
--------------------------

To customize an individual field, rather than rely on project level settings,
create a ``Countries`` subclass which overrides settings.

To override a setting, give the class an attribute matching the lowercased
setting without the ``COUNTRIES_`` prefix.

Then just reference this class in a field. For example, this ``CountryField``
uses a custom country list that only includes the G8 countries::

    from django_countries import Countries

    class G8Countries(Countries):
        only = [
            'CA', 'FR', 'DE', 'IT', 'JP', 'RU', 'GB',
            ('EU', _('European Union'))
        ]

    class Vote(models.Model):
        country = CountryField(countries=G8Countries)
        approve = models.BooleanField()


Django Rest Framework field
===========================

Django Countries ships with a ``CountryField`` serializer field to simplify
the REST interface. For example::

    from django_countries.serializer_fields import CountryField

    class PersonSerializer(serializers.ModelSerializer):
        country = CountryField()

        class Meta:
            model = models.Person
            fields = ('name', 'email', 'country')


You can optionally instantiate the field with ``countries`` with a custom
Countries_ instance.

.. _Countries: `Single field customization`_

REST output format
------------------

By default, the field will output just the country code. If you would rather
have more verbose output, instantiate the field with ``country_dict=True``,
which will result in the field having the following output structure::

    {"code": "NZ", "name": "New Zealand"}

Either the code or this dict output structure are acceptable as input
irregardless of the ``country_dict`` argument's value.
