import importlib.util

import pytest
from django.test import TestCase, override_settings
from rest_framework import serializers, views
from rest_framework.test import APIRequestFactory

from django_countries import countries
from django_countries.conf import settings
from django_countries.fields import Country
from django_countries.serializers import CountryFieldMixin
from django_countries.tests.custom_countries import FantasyCountries
from django_countries.tests.models import MultiCountry, Person

# Check for optional dependency for OpenAPI schema tests
HAS_DRF_SPECTACULAR = importlib.util.find_spec("drf_spectacular") is not None


def countries_display(countries):
    """
    Convert Countries into a DRF-OPTIONS formatted dict.
    """
    return [{"display_name": v, "value": k} for (k, v) in countries]


class PersonSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "name",
            "country",
            "other_country",
            "favourite_country",
            "fantasy_country",
        )
        extra_kwargs = {
            "other_country": {"country_dict": True},
            "favourite_country": {"name_only": True},
        }


class MultiCountrySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = MultiCountry
        fields = ("countries",)


class TestDRF(TestCase):
    def test_serialize(self):
        person = Person(name="Chris Beaven", country="NZ")
        serializer = PersonSerializer(person)
        self.assertEqual(
            serializer.data,
            {
                "name": "Chris Beaven",
                "country": "NZ",
                "other_country": "",
                "favourite_country": "New Zealand",
                "fantasy_country": "",
            },
        )

    def test_serialize_country_dict(self):
        person = Person(name="Chris Beaven", other_country="AU")
        serializer = PersonSerializer(person)
        self.assertEqual(
            serializer.data,
            {
                "name": "Chris Beaven",
                "country": "",
                "other_country": {"code": "AU", "name": "Australia"},
                "favourite_country": "New Zealand",
                "fantasy_country": "",
            },
        )

    def test_deserialize(self):
        serializer = PersonSerializer(
            data={"name": "Tester", "country": "US", "fantasy_country": "NV"}
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["country"], "US")

    def test_deserialize_country_dict(self):
        serializer = PersonSerializer(
            data={
                "name": "Tester",
                "country": {"code": "GB", "name": "Anything"},
                "fantasy_country": "NV",
            }
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["country"], "GB")

    def test_deserialize_by_name(self):
        serializer = PersonSerializer(
            data={
                "name": "Chris",
                "country": "New Zealand",
                "fantasy_country": "Neverland",
            }
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["country"], "NZ")
        self.assertEqual(serializer.validated_data["fantasy_country"], "NV")

    def test_deserialize_invalid(self):
        serializer = PersonSerializer(
            data={
                "name": "Chris",
                "country": "No Such Zealand",
                "fantasy_country": "Neverland",
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["country"], ['"No Such Zealand" is not a valid choice.']
        )

    def test_multi_serialize(self):
        mc = MultiCountry(countries="NZ,AU")
        serializer = MultiCountrySerializer(mc)
        self.assertEqual(serializer.data, {"countries": ["AU", "NZ"]})

    def test_multi_serialize_empty(self):
        mc = MultiCountry(countries="")
        serializer = MultiCountrySerializer(mc)
        self.assertEqual(serializer.data, {"countries": []})

    def test_multi_deserialize(self):
        serializer = MultiCountrySerializer(data={"countries": ["NZ", "AU"]})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["countries"], ["NZ", "AU"])

    def test_multi_deserialize_by_name(self):
        serializer = MultiCountrySerializer(
            data={"countries": ["New Zealand", "Australia"]}
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["countries"], ["NZ", "AU"])

    def test_multi_deserialize_invalid(self):
        serializer = MultiCountrySerializer(data={"countries": ["NZ", "BAD", "AU"]})
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors["countries"]
        if isinstance(errors, dict):
            # djangorestframework >= 3.8.0 returns errors as dict
            # with integers as keys
            errors = errors[1]
        self.assertEqual(errors, ['"BAD" is not a valid choice.'])

    def test_multi_deserialize_save(self):
        serializer = MultiCountrySerializer(data={"countries": ["NZ", "AU"]})
        self.assertTrue(serializer.is_valid())
        saved = serializer.save()
        loaded = MultiCountry.objects.get(pk=saved.pk)
        self.assertEqual(loaded.countries, [Country("AU"), Country("NZ")])

    def test_deserialize_blank_invalid(self):
        serializer = PersonSerializer(data={"name": "Chris", "country": ""})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["country"], ['"" is not a valid choice.'])


class TestDRFMetadata(TestCase):
    """
    Tests against the DRF OPTIONS API metadata endpoint.
    """

    @pytest.mark.skipif(not settings.USE_I18N, reason="No i18n")
    def test_actions(self):
        class ExampleView(views.APIView):
            """Example view."""

            def post(self, request):
                pass  # pragma: no cover

            def get_serializer(self):
                return PersonSerializer()

        def _choices(response, key):
            """Helper method for unpacking response JSON."""
            return response.data["actions"]["POST"][key]["choices"]

        view = ExampleView.as_view()

        factory = APIRequestFactory()
        request = factory.options("/")
        response = view(request=request)
        country_choices = _choices(response, "country")
        fantasy_choices_en = _choices(response, "fantasy_country")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(country_choices, countries_display(countries))
        self.assertEqual(fantasy_choices_en, countries_display(FantasyCountries()))

        with override_settings(LANGUAGE_CODE="fr"):
            response = view(request=request)
            fantasy_choices_fr = _choices(response, "fantasy_country")
            self.assertNotEqual(fantasy_choices_en, fantasy_choices_fr)


class TestDRFSchemaGeneration(TestCase):
    """
    Tests for OpenAPI schema generation with CountryField.
    """

    def test_country_dict_schema_annotation(self):
        """
        Test that CountryField with country_dict=True provides correct schema
        annotation. This is used by drf-spectacular for OpenAPI schema generation.
        """
        from django_countries.serializer_fields import CountryField

        # Test country_dict=True
        field = CountryField(country_dict=True)
        self.assertTrue(hasattr(field, "_spectacular_annotation"))
        annotation = field._spectacular_annotation
        self.assertIsNotNone(annotation)
        self.assertIn("field", annotation)
        schema = annotation["field"]
        self.assertEqual(schema["type"], "object")
        self.assertIn("properties", schema)
        self.assertIn("code", schema["properties"])
        self.assertIn("name", schema["properties"])
        self.assertEqual(schema["properties"]["code"]["type"], "string")
        self.assertEqual(schema["properties"]["name"]["type"], "string")
        self.assertEqual(schema["required"], ["code", "name"])

    def test_country_dict_schema_annotation_nullable(self):
        """
        Test that nullable CountryField with country_dict=True includes null in schema.
        """
        from django_countries.serializer_fields import CountryField

        field = CountryField(country_dict=True, allow_null=True)
        self.assertTrue(hasattr(field, "_spectacular_annotation"))
        annotation = field._spectacular_annotation
        self.assertIn("field", annotation)
        schema = annotation["field"]
        self.assertIsNotNone(schema)
        self.assertIn("oneOf", schema)
        # Should have object type and null type
        self.assertEqual(len(schema["oneOf"]), 2)
        # Check that one of them is the object schema
        object_schema = next(s for s in schema["oneOf"] if s.get("type") == "object")
        self.assertIn("properties", object_schema)
        self.assertIn("code", object_schema["properties"])
        # Check that one of them is null
        null_schema = next(s for s in schema["oneOf"] if s.get("type") == "null")
        self.assertEqual(null_schema["type"], "null")

    def test_name_only_schema_annotation(self):
        """
        Test that CountryField with name_only=True provides correct schema annotation.
        """
        from django_countries.serializer_fields import CountryField

        field = CountryField(name_only=True)
        self.assertTrue(hasattr(field, "_spectacular_annotation"))
        annotation = field._spectacular_annotation
        self.assertIn("field", annotation)
        schema = annotation["field"]
        self.assertIsNotNone(schema)
        self.assertEqual(schema["type"], "string")

    def test_name_only_schema_annotation_nullable(self):
        """
        Test that nullable CountryField with name_only=True includes null in schema.
        """
        from django_countries.serializer_fields import CountryField

        field = CountryField(name_only=True, allow_null=True)
        self.assertTrue(hasattr(field, "_spectacular_annotation"))
        annotation = field._spectacular_annotation
        self.assertIn("field", annotation)
        schema = annotation["field"]
        self.assertIsNotNone(schema)
        self.assertIn("oneOf", schema)
        self.assertEqual(len(schema["oneOf"]), 2)

    def test_standard_field_schema_annotation(self):
        """
        Test that standard CountryField doesn't set annotation.
        This allows the default ChoiceField enum handling to work.
        """
        from django_countries.serializer_fields import CountryField

        field = CountryField()
        # Standard field should not have _spectacular_annotation set
        self.assertFalse(hasattr(field, "_spectacular_annotation"))


@pytest.mark.skipif(not HAS_DRF_SPECTACULAR, reason="drf-spectacular not installed")
class TestDRFSpectacularIntegration(TestCase):
    """
    Integration tests with drf-spectacular for OpenAPI schema generation.
    """

    def test_spectacular_country_dict_generates_object_schema(self):
        """
        Test that drf-spectacular generates an object schema (not enum)
        for country_dict=True.
        """
        from drf_spectacular.openapi import AutoSchema

        from django_countries.serializer_fields import CountryField

        class TestSerializer(serializers.Serializer):
            country = CountryField(country_dict=True)

        # Use AutoSchema to map the field
        auto_schema = AutoSchema()
        field = TestSerializer().fields["country"]
        schema = auto_schema._map_serializer_field(field, "request", None)

        # Should be an object type, not an enum
        self.assertEqual(schema.get("type"), "object")
        self.assertIn("properties", schema)
        self.assertIn("code", schema["properties"])
        self.assertIn("name", schema["properties"])
        self.assertNotIn("enum", schema)

    def test_spectacular_name_only_generates_string_schema(self):
        """
        Test that drf-spectacular generates a string schema (not enum)
        for name_only=True.
        """
        from drf_spectacular.openapi import AutoSchema

        from django_countries.serializer_fields import CountryField

        class TestSerializer(serializers.Serializer):
            country = CountryField(name_only=True)

        auto_schema = AutoSchema()
        field = TestSerializer().fields["country"]
        schema = auto_schema._map_serializer_field(field, "request", None)

        # Should be a string type, not an enum
        self.assertEqual(schema.get("type"), "string")
        self.assertNotIn("enum", schema)

    def test_spectacular_standard_field_generates_enum_schema(self):
        """
        Test that drf-spectacular generates an enum schema for standard CountryField.
        """
        from drf_spectacular.openapi import AutoSchema

        from django_countries.serializer_fields import CountryField

        class TestSerializer(serializers.Serializer):
            country = CountryField()

        auto_schema = AutoSchema()
        field = TestSerializer().fields["country"]
        schema = auto_schema._map_serializer_field(field, "request", None)

        # Should be an enum
        self.assertIn("enum", schema)
        # Should have country codes
        self.assertIn("NZ", schema["enum"])
        self.assertIn("US", schema["enum"])
