# Change Log

This log shows interesting changes that happen for each version, latest
versions first. It can be assumed that translations have been updated each
release, and any new translations added.

<!-- towncrier release notes start -->

## 8.0.1 (11 November 2025)

### Bugfixes

- Fixed `required` attribute not being rendered on form widgets when using `COUNTRIES_FIRST_BREAK` setting. The separator option now correctly allows the field to remain required for HTML5 validation. ([#280](https://github.com/SmileyChris/django-countries/issues/280))
- Fixed Transifex translation pull workflow to use git commit timestamps instead of filesystem modification times, preventing translations from being incorrectly skipped. Updated German (de), Afrikaans (af), Slovak (sk), and Slovenian (sl) translations.

### Misc

- Add OLD_NAMES for Bahamas and Netherlands to support translation fallback when country names change. Updated translation workflow to generate English source locale and automatically push to Transifex during releases.


## 8.0.0 (4 November 2025)

**Note**: This release includes all changes from the yanked versions 7.8, 7.9, and 7.9.1, which were yanked because they inadvertently dropped Python 3.7 support without a major version bump.

### Features

- Added common names for six additional countries/territories: Democratic Republic of the Congo (CD), South Georgia (GS), Netherlands (NL), Palestine (PS), Saint Helena (SH), and Vatican City (VA). These provide friendlier, shorter names when `COUNTRIES_COMMON_NAMES` is enabled (default).

### Bugfixes

- Fix `COUNTRIES_OVERRIDE` to support custom country codes that are 3 characters long. Previously, 3-character codes were incorrectly treated as alpha3 codes and resolved to existing countries. ([#474](https://github.com/SmileyChris/django-countries/issues/474))
- Fixed TypeError "unhashable type: 'list'" when using CountryField(multiple=True) in Django admin list_display. ([#311](https://github.com/SmileyChris/django-countries/issues/311))
- Fixed CountryField(multiple=True) displaying "-" instead of country names in Django admin readonly_fields. ([#463](https://github.com/SmileyChris/django-countries/issues/463))
- Fixed incorrect max_length calculation for CountryField(multiple=True) when using COUNTRIES_FIRST with COUNTRIES_FIRST_REPEAT. ([#469](https://github.com/SmileyChris/django-countries/issues/469))
- Updated country names to match ISO 3166-1 OBP: Bahamas (The) and Netherlands (Kingdom of the). Also improved self_generate() regex to handle type hints in dictionary declarations.

### Improved Documentation

- Added MkDocs documentation site and simplified README to focus on quick start with link to full documentation.
- Consolidated release documentation into CONTRIBUTING.md and improved development setup instructions.
- Added documentation warning that CountryField does not support Django's `autocomplete_fields` in admin or third-party admin filter packages like `more_admin_filters`. ([#473](https://github.com/SmileyChris/django-countries/issues/473))
- Added comprehensive documentation on ISO 3166-1 country name formatting, explaining parentheses vs commas usage, capitalization of "the", and addressing common political objections about territories like Taiwan, Kosovo, Hong Kong, and Palestine.

### Deprecations and Removals

- Drop Python 3.7 support. Python 3.7 reached end-of-life in June 2023. The minimum supported Python version is now 3.8.

### Misc

- Expanded test matrix to cover Python 3.8-3.13 and Django 3.2-5.1 with improved test infrastructure.
- Fixed various code quality issues identified by ruff linter, including improved string formatting and file handling.
- Migrated build system from setuptools to uv_build for faster and more modern package building.
- Simplified release process with automated `just deploy` command and towncrier for changelog management.
- Fix unnecessary list comprehension in test_tags.py


## 7.9.1 (4 November 2025) [YANKED]

### Bugfixes

- Fix `COUNTRIES_OVERRIDE` to support custom country codes that are 3 characters long. Previously, 3-character codes were incorrectly treated as alpha3 codes and resolved to existing countries. ([#474](https://github.com/SmileyChris/django-countries/issues/474))

**Note**: This release was yanked because it inadvertently dropped Python 3.7 support without a major version bump. Use 8.0.0 or later instead.


## 7.9 (4 November 2025) [YANKED]

### Bugfixes

- Fixed TypeError "unhashable type: 'list'" when using CountryField(multiple=True) in Django admin list_display. ([#311](https://github.com/SmileyChris/django-countries/issues/311))
- Fixed CountryField(multiple=True) displaying "-" instead of country names in Django admin readonly_fields. ([#463](https://github.com/SmileyChris/django-countries/issues/463))
- Fixed incorrect max_length calculation for CountryField(multiple=True) when using COUNTRIES_FIRST with COUNTRIES_FIRST_REPEAT. ([#469](https://github.com/SmileyChris/django-countries/issues/469))

**Note**: This release was yanked because it inadvertently dropped Python 3.7 support without a major version bump. Use 8.0.0 or later instead.


## 7.8 (4 November 2025) [YANKED]

_Where'd 7.7 go? Well 7.6 was accidentally bumped to 7.8 because of the new release process!_

**Note**: This release was yanked because it inadvertently dropped Python 3.7 support without a major version bump. Use 8.0.0 or later instead.

### Improved Documentation

- Added MkDocs documentation site and simplified README to focus on quick start with link to full documentation.
- Consolidated release documentation into CONTRIBUTING.md and improved development setup instructions.

### Misc

- Expanded test matrix to cover Python 3.8-3.13 and Django 3.2-5.1 with improved test infrastructure.
- Fixed various code quality issues identified by ruff linter, including improved string formatting and file handling.
- Migrated build system from setuptools to uv_build for faster and more modern package building.
- Simplified release process with automated `just deploy` command and towncrier for changelog management.


## 7.6.1 (2 April 2024)

- Fix a TypeError when no country is selected, introduced in the Django 5 fix.


## 7.6 (27 March 2024)

- Replace deprecated `pkg_resources.iter_entry_points` with
  `importlib_metadata`.

- Support Django 5.0.

## 7.5.1 (1 February 2023)

- Make `CountryField` queryset filters also work with country codes in
  addition to names.

- Switch to `pyproject.toml` rather than `setup.py` to fix installation
  issues with pip 23.0+.


## 7.5 (12 December 2022)

- Rename Turkey to Türkiye.

- A change in v7.4 introduced multi-choice countries being stored sorted and
  deduplicated. This remains the default behaviour going forwards, but these
  can now be overridden via arguments on the `CountryField`.

- Improve translation fallback handling, fixing a threading race condition that
  could cause odd translation issues. Thanks to Jan Wróblewski and Antoine
  Fontaine for their help in resolving this.
  This also fixes translation issues with older Python 3.6/3.7 versions.

- Add Python 3.11, drop Python 3.6 and Django 2.2 support.


## 7.4.2 (10 October 2022)

- Fix error when using `USE_I18N = False`.


## 7.4.1 (7 October 2022)

- Fix broken translations due to last common country names fix.


## 7.4 (7 October 2022)

- Fixed Traditional Chinese translation (needed to be `locale/zh_Hant`).

- Update flag of Honduras.

- Add Django 4.0 and 4.1 to the test matrix, dropping 3.0 and 3.1

- Add Django Rest Framework 3.13 and 3.14, dropping 3.11.

- Multi-choice countries are now stored sorted and with duplicates stripped.
  Thanks flbraun and Jens Diemer!

- Fix common country names not being honoured in non-English translations (only
  fixed for Python 3.8+).


## 7.3.2 (4 March 2022)

- Fix slowdown introduced in v7.3 caused by always using country name lookups
  for field comparisons. `filter(country="New Zealand")` will no longer match
  now, but instead new `__name` and `__iname` filters have been added to
  achieve this.


## 7.3.1 (1 March 2022)

- Typing compatibility fixes for Python <3.9.


## 7.3 (28 February 2022)

- Make full English country names work in database lookups, for example,
  `Person.objects.filter(country__icontains="zealand")`.


## 7.2.1 (11 May 2021)

- Fix Latin translations.


## 7.2 (10 May 2021)

- Allow the character field to work with custom country codes that are not 2
  characters (such as "GB-WLS").

- Fix compatibility with `django-migrations-ignore-attrs` library.


## 7.1 (17 March 2021)

- Allow customising the `str_attr` of Country objects returned from a
  CountryField via a new `countries_str_attr` keyword argument (thanks C.
  Quentin).

- Add `pyuca` as an extra dependency, so that it can be installed like
  `pip install django-countries[pyuca]`.

- Add Django 3.2 support.


## 7.0 (5 December 2020)

- Add `name_only` as an option to the Django Rest Framework serializer field
  (thanks Miguel Marques).

- Add in Python typing.

- Add Python 3.9, Django 3.1, and Django Rest Framework 3.12 support.

- Drop Python 3.5 support.

- Improve IOC code functionality, allowing them to be overridden in
  `COUNTRIES_OVERRIDE` using the complex dictionary format.


## 6.1.3 (18 August 2020)

- Update flag of Mauritania.

- Add flag for Kosovo (under its temporary code of XK).


## 6.1.2 (26 March 2020)

- Fix Python 3.5 syntax error (no f-strings just yet...).


## 6.1.1 (26 March 2020)

- Change ISO country import so that "Falkland Islands  [Malvinas]" => "Falkland Islands (Malvinas)".


## 6.1 (20 March 2020)

- Add a GraphQL object type for a django `Country` object.


## 6.0 (28 February 2020)

- Make DRF CountryField respect `blank=False`. This is a backwards incompatible change since blank input will now
  return a validation error (unless `blank` is explicitly set to `True`).

- Fix `COUNTRIES_OVERRIDE` when using the complex dictionary format and a single name.

- Add bandit to the test suite for basic security analysis.

- Drop Python 2.7 and Python 3.4 support.

- Add Rest Framework 3.10 and 3.11 to the test matrix, remove 3.8.

- Fix a memory leak when using PyUCA. Thanks Meiyer (aka interDist)!


## 5.5 (11 September 2019)

- Django 3.0 compatibility.

- Plugin system for extending the `Country` object.


## 5.4 (11 August 2019)

- Renamed Macedonia -> North Macedonia.

- Fix an outlying `makemigrations` error.

- Pulled in new translations which were provided but missing from previous
  version.

- Fixed Simplified Chinese translation (needed to be `locale/zh_Hans`).

- Introduce an optional complex format for `COUNTRIES_ONLY` and
  `COUNTRIES_OVERRIDE` to allow for multiple names for a country, a custom
  three character code, and a custom numeric country code.


## 5.3.3 (16 February 2019)

- Add test coverage for Django Rest Framework 3.9.


## 5.3.2 (27 August 2018)

- Tests for Django 2.1 and Django Rest Framework 3.8.


## 5.3.1 (12 June 2018)

- Fix `dumpdata` and `loaddata` for `CountryField(multiple=True)`.


## 5.3 (20 April 2018)

- Iterating a `Countries` object now returns named tuples. This makes things
  nicer when using `{% get_countries %}` or using the country list elsewhere
  in your code.


## 5.2 (9 March 2018)

- Ensure Django 2.1 compatibility for `CountrySelectWidget`.

- Fix regression introduced into 5.1 when using Django 1.8 and certain queryset
  lookup types (like `__in`).


## 5.1.1 (31 January 2018)

- Fix some translations that were included in 5.1 but not compiled.


## 5.1 (30 January 2018)

* Tests now also cover Django Rest Framework 3.7 and Django 2.0.

* Allow for creating country fields using (valid) alpha-3 or numeric codes.

* Fix migration error with blank default (thanks Jens Diemer).

* Add a `{% get_countries %}` template tag (thanks Matija Čvrk).


## 5.0 (10 October 2017)

* No longer allow `multiple=True` and `null=True` together. This causes
  problems saving the field, and `null` shouldn't really be used anyway
  because the country field is a subclass of `CharField`.


## 4.6.2 (16 June 2017)


* Use transparency layer for flag sprites.


## 4.6.1 (16 June 2017)


* Fix invalid reStructuredText in CHANGES.

## 4.6 (16 June 2017)

* Add a `CountryFieldMixin` Django Rest Framework serializer mixin that
  automatically picks the right field type for a `CountryField` (both single
  and multi-choice).

* Validation for Django Rest Framework field (thanks Simon Meers).

* Allow case-insensitive `.by_name()` matching (thanks again, Simon).

* Ensure a multiple-choice `CountryField.max_length` is enough to hold all
  countries.

* Fix inefficient pickling of countries (thanks Craig de Stigter for the report
  and tests).

* Stop adding a blank choice when dealing with a multi-choice `CountryField`.

* Tests now cover multiple Django Rest Framework versions (back to 3.3).

## 4.5 (18 April 2017)

* Change rest framework field to be based on `ChoiceField`.

* Allow for the rest framework field to deserialize by full country name
  (specifically the English name for now).


## 4.4 (6 April 2017)

* Fix for broken CountryField on certain models in Django 1.11.
  Thanks aktiur for the test case.

* Update tests to cover Django 1.11


## 4.3 (29 March 2017)

* Handle "Czechia" translations in a nicer way (fall back to "Czech Republic"
  until new translations are available).

* Fix for an import error in Django 1.9+ due to use of non-lazy `ugettext` in
  the django-countries custom admin filter.

* Back to 100% test coverage.


## 4.2 (10 March 2017)

* Add sprite flag files (and `Country.flag_css` property) to help minimize
  HTTP requests.


## 4.1 (22 February 2017)

* Better default Django admin filter when filtering a country field in a
  `ModelAdmin`.

* Fix settings to support Django 1.11

* Fix when using a model instance with a deferred country field.

* Allow `CountryField` to handle multiple countries at once!

* Allow CountryField to still work if Deferred.

* Fix a field with customized country list. Thanks pilmie!


## 4.0.1 (16 August 2016)


* Fix tests for `COUNTRIES_FIRST_SORT` (feature still worked, tests didn't).


## 4.0 (16 August 2016)

Django supported versions are now 1.8+

* Drop legacy code

* Fix tests, 100% coverage

* IOS / OSX unicode flags function

* Fix widget choices on Django 1.9+

* Add `COUNTRIES_FIRST_SORT`. Thanks Edraak!

## 3.4.1 (22 October 2015)


* Fix minor packaging error.


## 3.4 (22 October 2015)

* Extend test suite to cover Django 1.8

* Fix XSS escaping issue in CountrySelectWidget

* Common name changes: fix typo of Moldova, add United Kingdom

* Add `{% get_country %}` template tag.

* New `CountryField` Django Rest Framework serializer field.

## 3.3 (30 Mar 2015)

* Add the attributes to `Countries` class that can override the default
  settings.

* CountriesField can now be passed a custom countries subclass to use, which
  combined with the previous change allows for different country choices for
  different fields.

* Allow `COUNTRIES_ONLY` to also accept just country codes in its list
  (rather than only two-tuples), looking up the translatable country name from
  the full country list.

* Fix Montenegro flag size (was 12px high rather than the standard 11px).

* Fix outdated ISO country name formatting for Bolivia, Gambia, Holy See,
  Iran, Micronesia, and Venezuela.


## 3.2 (24 Feb 2015)

* Fixes initial iteration failing for a fresh `Countries` object.

* Fix widget's flag URLs (and use ensure widget is HTML encoded safely).

* Add `countries.by_name(country, language='en')` method, allowing lookup of
  a country code by its full country name. Thanks Josh Schneier.


## 3.1.1 (15 Jan 2015)

* Packaging fix (`CHANGES.rst` wasn't in the manifest)


## 3.1 (15 Jan 2015)

* Start change log :)

* Add a `COUNTRIES_FIRST` setting (and some other related ones) to allow for
  specific countries to be shown before the entire alphanumeric list.

* Add a `blank_label` argument to `CountryField` to allow customization of
  the label shown in the initial blank choice shown in the select widget.

## 3.0.2 (29 Dec 2014)

* Fix `CountrySelectWidget` failing when used with a model form that is
  passed a model instance.


## 3.0.1 (27 Oct 2014)

* Revert descriptor to always return a Country object.

* Fix the `CountryField` widget choices appearing empty due to a translation
  change in v3.0.

## 3.0 (22 Oct 2014)

Django supported versions are now 1.4 (LTS) and 1.6+

* Add `COUNTRIES_ONLY` setting to restrict to a specific list of countries.

* Optimize country name translations to avoid exessive translation calls that
  were causing a notable performance impact.

* PyUCA integration, allowing for more accurate sorting across all locales.
  Also, a better sorting method when PyUCA isn't installed.

* Better tests (now at 100% test coverage).

* Add a `COUNTRIES_FLAG_URL` setting to allow custom flag urls.

* Support both IOC and numeric country codes, allowing more flexible lookup of
  countries and specific code types.

* Field descriptor now returns `None` if no country matches (*reverted in
  v3.0.1*)

## 2.1.2 (28 Mar 2014)

* Fix Python 3 compatibility.



## 2.1.1 (28 Mar 2014)

* Fix issue with translations getting evaluated early.

## 2.1 (24 Mar 2014)

* Add IOC (3 letter) country codes.

* Fix bug when loading fixtures.

## 2.0 (18 Feb 2014)

This is the first entry to the change log. The previous was 1.5,
released 19 Nov 2012.

* Optimized flag images, adding flags missing from original source.

* Better storage of settings and country list.

* New country list format for fields.

* Better tests.

* Changed `COUNTRIES_FLAG_STATIC` setting to `COUNTRIES_FLAG_URL`.
