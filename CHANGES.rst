==========
Change Log
==========

This log shows interesting changes that happen for each version, latest
versions first. It can be assumed that translations have been updated each
release (and any new translations added).

Version 4.6 (16 June 2017)
==========================

* Add a ``CountryFieldMixin`` Django Rest Framework serializer mixin that
  automatically picks the right field type for a ``CountryField`` (both single
  and multi-choice).

* Validation for Django Rest Framework field (thanks Simon Meers).

* Allow case-insensitive ``.by_name()`` matching (thanks again, Simon).

* Ensure a multiple-choice ``CountryField.max_length`` is enough to hold all
  countries.

* Fix inefficient pickling of countries (thanks Craig de Stigter for the report
  and tests).

* Stop adding a blank choice when dealing with a multi-choice ``CountryField``.

* Tests now cover multiple Django Rest Framework versions (back to 3.3).

Version 4.6.1
-------------

* Fix invalid reStructuredText in CHANGES.


Version 4.5 (18 April 2017)
===========================

* Change rest framework field to be based on ``ChoiceField``.

* Allow for the rest framework field to deserialize by full country name
  (specifically the English name for now).


Version 4.4 (6 April 2017)
==========================

* Fix for broken CountryField on certain models in Django 1.11.
  Thanks aktiur for the test case.

* Update tests to cover Django 1.11


Version 4.3 (29 March 2017)
===========================

* Handle "Czechia" translations in a nicer way (fall back to "Czech Republic"
  until new translations are available).

* Fix for an import error in Django 1.9+ due to use of non-lazy ``ugettext`` in
  the django-countries custom admin filter.

* Back to 100% test coverage.


Version 4.2 (10 March 2017)
===========================

* Add sprite flag files (and ``Country.flag_css`` property) to help minimize
  HTTP requests.


Version 4.1 (22 February 2017)
==============================

* Better default Django admin filter when filtering a country field in a
  ``ModelAdmin``.

* Fix settings to support Django 1.11

* Fix when using a model instance with a deferred country field.

* Allow ``CountryField`` to handle multiple countries at once!

* Allow CountryField to still work if Deferred.

* Fix a field with customized country list. Thanks pilmie!


Version 4.0 (16 August 2016)
============================

Django supported versions are now 1.8+

* Drop legacy code

* Fix tests, 100% coverage

* IOS / OSX unicode flags function

* Fix widget choices on Django 1.9+

* Add ``COUNTRIES_FIRST_SORT``. Thanks Edraak!

Version 4.0.1
-------------

* Fix tests for ``COUNTRIES_FIRST_SORT`` (feature still worked, tests didn't).


Version 3.4 (22 October 2015)
=============================

* Extend test suite to cover Django 1.8

* Fix XSS escaping issue in CountrySelectWidget

* Common name changes: fix typo of Moldova, add United Kingdom

* Add ``{% get_country %}`` template tag.

* New ``CountryField`` Django Rest Framework serializer field.

Version 3.4.1
-------------

* Fix minor packaging error.


Version 3.3 (30 Mar 2015)
=========================

* Add the attributes to ``Countries`` class that can override the default
  settings.

* CountriesField can now be passed a custom countries subclass to use, which
  combined with the previous change allows for different country choices for
  different fields.

* Allow ``COUNTRIES_ONLY`` to also accept just country codes in its list
  (rather than only two-tuples), looking up the translatable country name from
  the full country list.

* Fix Montenegro flag size (was 12px high rather than the standard 11px).

* Fix outdated ISO country name formatting for Bolivia, Gambia, Holy See,
  Iran, Micronesia, and Venezuela.


Version 3.2 (24 Feb 2015)
=========================

* Fixes initial iteration failing for a fresh ``Countries`` object.

* Fix widget's flag URLs (and use ensure widget is HTML encoded safely).

* Add ``countries.by_name(country, language='en')`` method, allowing lookup of
  a country code by its full country name. Thanks Josh Schneier.


Version 3.1 (15 Jan 2015)
=========================

* Start change log :)

* Add a ``COUNTRIES_FIRST`` setting (and some other related ones) to allow for
  specific countries to be shown before the entire alphanumeric list.

* Add a ``blank_label`` argument to ``CountryField`` to allow customization of
  the label shown in the initial blank choice shown in the select widget.

Version 3.1.1 (15 Jan 2015)
---------------------------

* Packaging fix (``CHANGES.rst`` wasn't in the manifest)


Version 3.0 (22 Oct 2014)
=========================

Django supported versions are now 1.4 (LTS) and 1.6+

* Add ``COUNTRIES_ONLY`` setting to restrict to a specific list of countries.

* Optimize country name translations to avoid exessive translation calls that
  were causing a notable performance impact.

* PyUCA integration, allowing for more accurate sorting across all locales.
  Also, a better sorting method when PyUCA isn't installed.

* Better tests (now at 100% test coverage).

* Add a ``COUNTRIES_FLAG_URL`` setting to allow custom flag urls.

* Support both IOC and numeric country codes, allowing more flexible lookup of
  countries and specific code types.

* Field descriptor now returns ``None`` if no country matches (*reverted in v3.0.1*)

Version 3.0.1 (27 Oct 2014)
---------------------------

* Revert descriptor to always return a Country object.

* Fix the ``CountryField`` widget choices appearing empty due to a translation
  change in v3.0.

Version 3.0.2 (29 Dec 2014)
---------------------------

* Fix ``CountrySelectWidget`` failing when used with a model form that is
  passed a model instance.


Version 2.1 (24 Mar 2014)
=========================

* Add IOC (3 letter) country codes.

* Fix bug when loading fixtures.

Version 2.1.1 (28 Mar 2014)
---------------------------

* Fix issue with translations getting evaluated early.

Version 2.1.2 (28 Mar 2014)
---------------------------

* Fix Python 3 compatibility.



Version 2.0 (18 Feb 2014)
=========================

This is the first entry to the change log. The previous version was 1.5,
released 19 Nov 2012.

* Optimized flag images, adding flags missing from original source.

* Better storage of settings and country list.

* New country list format for fields.

* Better tests.

* Changed ``COUNTRIES_FLAG_STATIC`` setting to ``COUNTRIES_FLAG_URL``.
