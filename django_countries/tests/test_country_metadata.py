from django.test import TestCase

from django_countries.fields import Country
from django_countries.utils.metadata import get_metadata


class CountryMetadataTest(TestCase):
    def test_gb_metadata(self):
        country = Country("GB")
        self.assertEqual(country.currency_name, "British pound")
        self.assertEqual(country.currency_symbol, "£")
        self.assertEqual(country.calling_code, "+44")
        self.assertEqual(country.utc_offset, "+00:00")
        self.assertEqual(country.capital_city, "London")
        self.assertEqual(country.continent, "Europe")
        self.assertEqual(country.date_format, "DD/MM/YYYY")
        self.assertEqual(country.official_language, ["English"])

    def test_us_metadata(self):
        country = Country("US")
        self.assertEqual(country.currency_name, "United States dollar")
        self.assertEqual(country.currency_symbol, "$")
        self.assertEqual(country.capital_city, "Washington, D.C.")

    def test_ng_metadata(self):
        country = Country("NG")
        self.assertEqual(country.currency_name, "Naira")
        self.assertEqual(country.currency_symbol, "₦")
        self.assertEqual(country.capital_city, "Abuja")

    def test_invalid_country_raises_keyerror(self):
        country = Country("XX")
        with self.assertRaises(KeyError):
            _ = country.currency_name

    def test_caching(self):
        metadata1 = get_metadata()
        metadata2 = get_metadata()
        self.assertIs(metadata1, metadata2)
