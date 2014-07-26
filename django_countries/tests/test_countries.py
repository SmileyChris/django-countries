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

    def test_countries_custom_removed_len(self):
        with self.settings(COUNTRIES_OVERRIDE={'AU': None}):
            self.assertEqual(len(countries), self.EXPECTED_COUNTRY_COUNT - 1)

    def test_countries_custom_added_len(self):
        with self.settings(COUNTRIES_OVERRIDE={'XX': 'Neverland'}):
            self.assertEqual(len(countries), self.EXPECTED_COUNTRY_COUNT + 1)

    def test_countries_getitem(self):
        try:
            country = countries[0]
        except TypeError as e:
            self.fail(e.message)

    def test_countries_slice(self):
        try:
            sliced = countries[10:20:2]
        except TypeError as e:
            self.fail(e.message)
        self.assertEqual(len(sliced), 5)

    def test_countries_custom_ugettext_evaluation(self):

        class FakeLazyUGetText(object):

            def __bool__(self):
                raise ValueError("Can't evaluate lazy_ugettext yet")

            __nonzero__ = __bool__

        with self.settings(COUNTRIES_OVERRIDE={'AU': FakeLazyUGetText()}):
            countries.countries

    def test_ioc_countries(self):
        from ..ioc_data import check_ioc_countries
        check_ioc_countries()

    def test_flags(self):
        from ..data import check_flags
        check_flags()
