================
Django Countries
================

.. image:: https://badge.fury.io/py/django-countries.svg
    :alt: PyPI version
    :target: https://badge.fury.io/py/django-countries

.. image:: https://travis-ci.org/SmileyChris/django-countries.svg?branch=master
    :alt: Build status
    :target: http://travis-ci.org/SmileyChris/django-countries

.. image:: https://codecov.io/gh/SmileyChris/django-countries/branch/master/graph/badge.svg
    :alt: Coverage status
    :target: https://codecov.io/gh/SmileyChris/django-countries


A Django application that provides country choices for use with forms, flag
icons static files, and a country field for models.

.. contents::
    :local:
    :backlinks: none


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

Consider the following model using a ``CountryField``:

.. code:: python

    from django.db import models
    from django_countries.fields import CountryField

    class Person(models.Model):
        name = models.CharField(max_length=100)
        country = CountryField()

Any ``Person`` instance will have a ``country`` attribute that you can use to
get details of the person's country:

.. code:: python

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
forms:

.. code:: python

    country = CountryField(blank_label='(select country)')


Multi-choice
------------

This field can also allow multiple selections of countries (saved as a comma
separated string). The field will always output a list of countries in this
mode. For example:

.. code:: python

    class Incident(models.Model):
        title = models.CharField(max_length=100)
        countries = CountryField(multiple=True)

    >>> for country in Incident.objects.get(title='Pavlova dispute').countries:
    ...     print(country.name)
    Australia
    New Zealand


The ``Country`` object
----------------------

An object used to represent a country, instantiated with a two character
country code, three character code, or numeric code.

It can be compared to other objects as if it was a string containing the
country code and when evaluated as text, returns the country code.

name
  Contains the full country name.

flag
  Contains a URL to the flag. If you page could have lots of different flags
  then consider using ``flag_css`` instead to avoid excessive HTTP requests.

flag_css
  Output the css classes needed to display an HTML element as the correct flag
  from within a single sprite image that contains all flags. For example:

  .. code:: jinja

    <link rel="stylesheet" href="{% static 'flags/sprite.css' %}">
    <i class="{{ country.flag_css }}"></i>

  For multiple flag resolutions, use ``sprite-hq.css`` instead and add the
  ``flag2x``, ``flag3x``, or ``flag4x`` class. For example:

  .. code:: jinja

    <link rel="stylesheet" href="{% static 'flags/sprite-hq.css' %}">
    Normal: <i class="{{ country.flag_css }}"></i>
    Bigger: <i class="flag2x {{ country.flag_css }}"></i>

  You might also want to consider using ``aria-label`` for better
  accessibility:

  .. code:: jinja

    <i class="{{ country.flag_css }}"
        aria-label="{% blocktrans with country_code=country.code %}
            {{ country_code }} flag
        {% endblocktrans %}"></i>

unicode_flag
  A unicode glyph for the flag for this country. Currently well-supported in
  iOS and OS X. See https://en.wikipedia.org/wiki/Regional_Indicator_Symbol
  for details.

code
  The two letter country code for this country.

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

When you create your form, you can use this custom widget like normal:

.. code:: python

    from django_countries.widgets import CountrySelectWidget

    class PersonForm(forms.ModelForm):
        class Meta:
            model = models.Person
            fields = ('name', 'country')
            widgets = {'country': CountrySelectWidget()}

Pass a ``layout`` text argument to the widget to change the positioning of the
flag and widget. The default layout is:

.. code:: python

    '{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'


Custom forms
============

If you want to use the countries in a custom form, use the model field's custom
form field to ensure the translatable strings for the country choices are left
lazy until the widget renders:

.. code:: python

    from django_countries.fields import CountryField

    class CustomForm(forms.Form):
        country = CountryField().formfield()

Use ``CountryField(blank=True)`` for non-required form fields, and
``CountryField(blank_label='(Select country)')`` to use a custom label for the
initial blank option.

You can also use the CountrySelectWidget_ as the widget for this field if you
want the flag image after the select box.


Get the countries from Python
=============================

Use the ``django_countries.countries`` object instance as an iterator of ISO
3166-1 country codes and names (sorted by name).

For example:

.. code:: python

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
of its properties:

.. code:: jinja

    {% load countries %}
    {% get_country 'BR' as country %}
    {{ country.name }}

If you need a list of countries, there's also a simple tag for that:

.. code:: jinja

    {% load countries %}
    {% get_countries as countries %}
    <select>
    {% for country in countries %}
        <option value="{{ country.code }}">{{ country.name }}</option>
    {% endfor %}
    </select>


Customization
=============

Customize the country list
--------------------------

Country names are taken from the official ISO 3166-1 list. If your project
requires the use of alternative names, the inclusion or exclusion of specific
countries then use the ``COUNTRIES_OVERRIDE`` setting.

A dictionary of names to override the defaults. The values can also use a more
`complex dictionary format`_.

Note that you will need to handle translation of customised country names.

Setting a country's name to ``None`` will exclude it from the country list.
For example:

.. code:: python

    from django.utils.translation import ugettext_lazy as _

    COUNTRIES_OVERRIDE = {
        'NZ': _('Middle Earth'),
        'AU': None,
        'US': {'names': [
            _('United States of America'),
            _('America'),
        ],
    }

If you have a specific list of countries that should be used, use
``COUNTRIES_ONLY``:

.. code:: python

    COUNTRIES_ONLY = ['NZ', 'AU']

or to specify your own country names, use a dictionary or two-tuple list
(string items will use the standard country name):

.. code:: python

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

Alternatively, you can specify a different URL on a specific ``CountryField``:

.. code:: python

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
uses a custom country list that only includes the G8 countries:

.. code:: python

    from django_countries import Countries

    class G8Countries(Countries):
        only = [
            'CA', 'FR', 'DE', 'IT', 'JP', 'RU', 'GB',
            ('EU', _('European Union'))
        ]

    class Vote(models.Model):
        country = CountryField(countries=G8Countries)
        approve = models.BooleanField()


Complex dictionary format
-------------------------

For ``COUNTRIES_ONLY`` and ``COUNTRIES_OVERRIDE``, you can also provide a
dictionary rather than just a translatable string for the country name.

The options within the dictionary are:

``name`` or ``names`` (required)
  Either a single translatable name for this country or a list of multiple
  translatable names. If using multiple names, the first name takes preference
  when using ``COUNTRIES_FIRST`` or the ``Country.name``.

``alpha3`` (optional)
  An ISO 3166-1 three character code (or an empty string to nullify an existing
  code for this country.

``numeric`` (optional)
  An ISO 3166-1 numeric country code (or ``None`` to nullify an existing code
  for this country. The numeric codes 900 to 999 are left available by the
  standard for user-assignment.


Django Rest Framework
=====================

Django Countries ships with a ``CountryFieldMixin`` to make the
`CountryField`_ model field compatible with DRF serializers. Use the following
mixin with your model serializer:

.. code:: python

    from django_countries.serializers import CountryFieldMixin

    class CountrySerializer(CountryFieldMixin, serializers.ModelSerializer):

        class Meta:
            model = models.Person
            fields = ('name', 'email', 'country')

This mixin handles both standard and `multi-choice`_ country fields.


Django Rest Framework field
---------------------------

For lower level use (or when not dealing with model fields), you can use the
included ``CountryField`` serializer field. For example:

.. code:: python

    from django_countries.serializer_fields import CountryField

    class CountrySerializer(serializers.Serializer):
        country = CountryField()

You can optionally instantiate the field with the ``countries`` argument to
specify a custom Countries_ instance.

.. _Countries: `Single field customization`_

REST output format
^^^^^^^^^^^^^^^^^^

By default, the field will output just the country code. If you would rather
have more verbose output, instantiate the field with ``country_dict=True``,
which will result in the field having the following output structure:

.. code:: json

    {"code": "NZ", "name": "New Zealand"}

Either the code or this dict output structure are acceptable as input
irregardless of the ``country_dict`` argument's value.


OPTIONS request
---------------

When you request OPTIONS against a resource (using the DRF `metadata support`_)
the countries will be returned in the response as choices:

.. code:: text

    OPTIONS /api/address/ HTTP/1.1

    HTTP/1.1 200 OK
    Content-Type: application/json
    Allow: GET, POST, HEAD, OPTIONS

    {
    "actions": {
      "POST": {
        "country": {
        "type": "choice",
        "label": "Country",
        "choices": [
          {
            "display_name": "Australia",
            "value": "AU"
          },
          [...]
          {
            "display_name": "United Kingdom",
            "value": "GB"
          }
        ]
      }
    }

.. _metadata support: http://www.django-rest-framework.org/api-guide/metadata/
