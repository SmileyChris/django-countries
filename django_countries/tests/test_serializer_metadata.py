from django.test import TestCase
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from django_countries.fields import Country

class CountrySerializerMetadataTest(TestCase):
    class CountrySerializer(serializers.Serializer):
        country = CountryField(country_dict=True)

    class AllMetadataSerializer(serializers.Serializer):
        country = CountryField(country_dict=[
            "code", "name", "currency_name", "currency_symbol", 
            "calling_code", "utc_offset", "capital_city", 
            "continent", "date_format", "official_language", "timezones"
        ])

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
