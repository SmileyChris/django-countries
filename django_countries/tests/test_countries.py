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

    def test_countries_custom_ugettext_evaluation(self):

        class FakeLazyUGetText(object):

            def __bool__(self):
                raise ValueError("Can't evaluate lazy_ugettext yet")

            __nonzero__ = __bool__

        with self.settings(COUNTRIES_OVERRIDE={'AU': FakeLazyUGetText()}):
            countries.countries
