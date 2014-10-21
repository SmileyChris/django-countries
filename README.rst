================
Django Countries
================

A Django application that provides country choices for use with forms, flag
icons static files, and a country field for models.

Installation
=============================

1. ``pip install django-countries``
2. Add ``django_countries`` to ``INSTALLED_APPS``


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
            widgets = {'country': CountrySelectWidget}


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
