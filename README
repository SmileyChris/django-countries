================
django-countries
================

A Django application which provides country choices for use with forms, and
a country field for models.

To use the flags, use the ``django.contrib.staticfiles`` app added in Django
1.3 (or `django-staticfiles`_ application for previous Django versions).

.. _django-staticfiles: http://pypi.python.org/pypi/django-staticfiles/


CountryField
============

A country field for Django models that provides all ISO 3166-1 countries as
choices.

``CountryField`` is based on Django's ``CharField``, providing choices
corresponding to the official ISO 3166-1 list of countries (with a default
``max_length`` of 2).

Consider the following model using a ``CountryField``::

    from django.db import models
    from django_countries import CountryField

    class Person(models.Model):
        name = models.CharField(max_length=100)
        country = CountryField()

Any ``Person`` instance will have a ``country`` attribute that you can use to
get details of the person's country:

>>> person = Person(name='Chris', country='NZ')
>>> person.country
Country(code='NZ')
>>> person.country.name
u'New Zealand'
>>> person.country.flag
u'/static/flags/nz.gif'

This object (``person.country`` in the example) is a ``Country`` instance,
which is described below.

The ``Country`` object
----------------------

An object used to represent a country, instanciated with a two character
country code.

It can be compared to other objects as if it was a string containing the
country code, and it's ``__unicode__`` method returns the country code.  

name
  Contains the full country name.

flag
  Contains a URL to the flag. ``'flags/[lowercasecountrycode].gif'`` is
  appended to the ``STATIC_URL`` setting, or if that isn't set, the
  ``MEDIA_URL`` setting.


Country Choices
===============

The ``django_countries.countries`` module contains some constants which can be
used to generate choices lists for a Django ``Select`` form field.

``COUNTRIES``
  A tuple of two part tuples, each consisting of a country code and the
  corresponding nicely titled (and translatable) country name.

``COUNTRIES_PLUS``
  A tuple, similar to ``COUNTRIES``, but also includes duplicates for countries
  that contain a comma (i.e. the non-comma'd version).

``OFFICIAL_COUNTRIES``
  A dictionary where each key is a country code and each value is the
  corresponding official capitalised ISO 3166-1 English country name.
