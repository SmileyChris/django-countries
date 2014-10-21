# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

from django_countries import countries


class TestCountriesObject(TestCase):
    EXPECTED_COUNTRY_COUNT = 249

    def setUp(self):
        del countries.countries

    def tearDown(self):
        del countries.countries

    def test_countries_len(self):
        self.assertEqual(len(countries), self.EXPECTED_COUNTRY_COUNT)

    def test_countries_sorted(self):
        self.assertEqual(
            list(countries)[:3],
            [
                ('AF', 'Afghanistan'),
                ('AX', 'Åland Islands'),
                ('AL', 'Albania'),
            ])

    def test_countries_custom_removed_len(self):
        with self.settings(COUNTRIES_OVERRIDE={'AU': None}):
            self.assertEqual(len(countries), self.EXPECTED_COUNTRY_COUNT - 1)

    def test_countries_custom_added_len(self):
        with self.settings(COUNTRIES_OVERRIDE={'XX': 'Neverland'}):
            self.assertEqual(len(countries), self.EXPECTED_COUNTRY_COUNT + 1)

    def test_countries_getitem(self):
        countries[0]

    def test_countries_slice(self):
        sliced = countries[10:20:2]
        self.assertEqual(len(sliced), 5)

    def test_countries_custom_ugettext_evaluation(self):

        class FakeLazyUGetText(object):

            def __bool__(self):  # pragma: no cover
                raise ValueError("Can't evaluate lazy_ugettext yet")

            __nonzero__ = __bool__

        with self.settings(COUNTRIES_OVERRIDE={'AU': FakeLazyUGetText()}):
            countries.countries

    def test_ioc_countries(self):
        from ..ioc_data import check_ioc_countries
        check_ioc_countries(verbosity=0)

    def test_flags(self):
        from ..data import check_flags
        check_flags(verbosity=0)

    def test_common_names(self):
        from ..data import check_common_names
        check_common_names()

    def test_alpha2(self):
        self.assertEqual(countries.alpha2('NZ'), 'NZ')
        self.assertEqual(countries.alpha2('nZ'), 'NZ')
        self.assertEqual(countries.alpha2('Nzl'), 'NZ')
        self.assertEqual(countries.alpha2(554), 'NZ')
        self.assertEqual(countries.alpha2('554'), 'NZ')

    def test_alpha2_invalid(self):
        self.assertEqual(countries.alpha2('XX'), '')

    def test_alpha2_override(self):
        with self.settings(COUNTRIES_OVERRIDE={'AU': None}):
            self.assertEqual(countries.alpha2('AU'), '')

    def test_alpha2_override_new(self):
        with self.settings(COUNTRIES_OVERRIDE={'XX': 'Neverland'}):
            self.assertEqual(countries.alpha2('XX'), 'XX')
