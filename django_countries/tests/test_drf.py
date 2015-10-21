from __future__ import unicode_literals

from django.test import TestCase
from rest_framework import serializers

from django_countries.tests.models import Person
from django_countries.serializer_fields import CountryField


class PersonSerializer(serializers.ModelSerializer):
    country = CountryField()
    other_country = CountryField(country_dict=True, required=False)

    class Meta:
        model = Person
        fields = ('name', 'country', 'other_country')


class TestDRF(TestCase):

    def test_serialize(self):
        person = Person(name='Chris Beaven', country='NZ')
        serializer = PersonSerializer(person)
        self.assertEqual(
            serializer.data,
            {'name': 'Chris Beaven', 'country': 'NZ', 'other_country': ''})

    def test_serialize_country_dict(self):
        person = Person(name='Chris Beaven', other_country='AU')
        serializer = PersonSerializer(person)
        self.assertEqual(
            serializer.data,
            {
                'name': 'Chris Beaven',
                'country': '',
                'other_country': {'code': 'AU', 'name': 'Australia'},
            })

    def test_deserialize(self):
        serializer = PersonSerializer(data={'name': 'Tester', 'country': 'US'})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['country'], 'US')

    def test_deserialize_country_dict(self):
        serializer = PersonSerializer(data={
            'name': 'Tester', 'country': {'code': 'GB', 'name': 'Anything'}})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['country'], 'GB')
