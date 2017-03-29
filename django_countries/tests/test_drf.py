from __future__ import unicode_literals

from django.test import TestCase

from django_countries import countries
from django_countries.tests.models import Person
from django_countries.tests.custom_countries import FantasyCountries
from django_countries.serializer_fields import CountryField

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework import serializers, views


def countries_display(countries):
    """Convert Countries into a DRF-OPTIONS formatted dict."""
    return [{'display_name': v, 'value': k} for (k, v) in countries]


class PersonSerializer(serializers.ModelSerializer):
    country = CountryField()
    other_country = CountryField(country_dict=True, required=False)
    favourite_country = CountryField(countries=FantasyCountries)

    class Meta:
        model = Person
        fields = ('name', 'country', 'other_country', 'favourite_country')


class TestDRF(TestCase):

    def test_serialize(self):
        person = Person(name='Chris Beaven', country='NZ')
        serializer = PersonSerializer(person)
        self.assertEqual(
            serializer.data,
            {
                'name': 'Chris Beaven',
                'country': 'NZ',
                'other_country': '',
                'favourite_country': 'NZ'
            })

    def test_serialize_country_dict(self):
        person = Person(name='Chris Beaven', other_country='AU')
        serializer = PersonSerializer(person)
        self.assertEqual(
            serializer.data,
            {
                'name': 'Chris Beaven',
                'country': '',
                'other_country': {'code': 'AU', 'name': 'Australia'},
                'favourite_country': 'NZ'
            })

    def test_deserialize(self):
        serializer = PersonSerializer(data={
            'name': 'Tester',
            'country': 'US',
            'favourite_country': 'NV'
        })
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['country'], 'US')

    def test_deserialize_country_dict(self):
        serializer = PersonSerializer(data={
            'name': 'Tester',
            'country': {'code': 'GB', 'name': 'Anything'},
            'favourite_country': 'NV'
        })
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['country'], 'GB')


class TestDRFMetadata(TestCase):

    """Tests against the DRF OPTIONS API metadata endpoint."""

    def test_actions(self):

        class ExampleView(views.APIView):
            """Example view."""
            def post(self, request):
                pass

            def get_serializer(self):
                return PersonSerializer()

        request = Request(APIRequestFactory().options('/'))
        view = ExampleView.as_view()
        response = view(request=request)
        country_choices = response.data['actions']['POST']['country']['choices']
        favourite_choices = response.data['actions']['POST']['favourite_country']['choices']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(country_choices, countries_display(countries))
        self.assertEqual(favourite_choices, countries_display(FantasyCountries()))
