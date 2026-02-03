from django.test import TestCase
from rest_framework import serializers

from django_countries.serializer_fields import CountryField


class CountrySerializerMetadataTest(TestCase):
    class CountrySerializer(serializers.Serializer):
        country: CountryField = CountryField(country_dict=True)

    class AllMetadataSerializer(serializers.Serializer):
        country: CountryField = CountryField(
            country_dict=[
                "code",
                "name",
                "currency_name",
                "currency_symbol",
                "calling_code",
                "utc_offset",
                "capital_city",
                "continent",
                "date_format",
                "official_language",
                "timezones",
            ]
        )

    def test_country_dict_default_metadata(self):
        serializer = self.CountrySerializer(instance={"country": "GB"})
        data = serializer.data["country"]
        self.assertEqual(data["code"], "GB")
        self.assertEqual(data["name"], "United Kingdom")

    def test_all_metadata_keys(self):
        serializer = self.AllMetadataSerializer(instance={"country": "GB"})
        data = serializer.data["country"]

        self.assertEqual(data["code"], "GB")
        self.assertEqual(data["name"], "United Kingdom")
        self.assertEqual(data["currency_name"], "British pound")
        self.assertEqual(data["currency_symbol"], "£")
        self.assertEqual(data["calling_code"], "+44")
        self.assertEqual(data["utc_offset"], "+00:00")
        self.assertEqual(data["capital_city"], "London")
        self.assertEqual(data["continent"], "Europe")
        self.assertEqual(data["date_format"], "DD/MM/YYYY")
        self.assertEqual(data["official_language"], ["English"])
        self.assertEqual(data["timezones"], [])

    def test_invalid_metadata_key(self):
        with self.assertRaises(ValueError) as cm:
            CountryField(country_dict=["invalid_key"])
        self.assertIn("Unsupported country_dict key 'invalid_key'", str(cm.exception))

    def test_invalid_country_dict_type(self):
        with self.assertRaises(TypeError) as cm:
            CountryField(country_dict=123)
        self.assertIn(
            "country_dict must be a boolean or an iterable of keys", str(cm.exception)
        )

    def test_empty_country_dict_iterable(self):
        with self.assertRaises(ValueError) as cm:
            CountryField(country_dict=iter([]))
        self.assertIn(
            "country_dict iterable must include at least one key", str(cm.exception)
        )

    def test_non_string_key_in_country_dict(self):
        with self.assertRaises(TypeError) as cm:
            CountryField(country_dict=["name", 123])
        self.assertIn("country_dict keys must be strings", str(cm.exception))

    def test_empty_string_key_in_country_dict(self):
        with self.assertRaises(ValueError) as cm:
            CountryField(country_dict=["name", ""])
        self.assertIn("country_dict keys must be non-empty strings", str(cm.exception))
