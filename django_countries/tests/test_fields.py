from __future__ import unicode_literals
from django.test import TestCase
from django_countries.tests.models import Person
from django.utils.encoding import force_text


class TestCountryField(TestCase):

    def create_person(self, country='NZ'):
        return Person.objects.create(name='Chris Beaven', country='NZ')

    def test_logic(self):
        person = Person(name='Chris Beaven', country='NZ')

        self.assertEqual(person.country, 'NZ')
        self.assertNotEqual(person.country, 'ZZ')

        self.assertTrue(person.country < 'OA')
        self.assertTrue(person.country > 'NY')

        self.assertTrue(person.country)
        person.country = ''
        self.assertFalse(person.country)

    def test_text(self):
        person = Person(name='Chris Beaven', country='NZ')
        self.assertEqual(force_text(person.country), 'NZ')

    def test_name(self):
        person = Person(name='Chris Beaven', country='NZ')
        self.assertEqual(person.country.name, u'New Zealand')

    def test_flag(self):
        person = Person(name='Chris Beaven', country='NZ')
        self.assertEqual(person.country.flag, '/static/flags/nz.gif')

    def test_blank(self):
        person = Person.objects.create(name='The Outsider', country=None)
        self.assertEqual(person.country, '')

        person = Person.objects.get(pk=person.pk)
        self.assertEqual(person.country, '')

    def test_len(self):
        person = Person(name='Chris Beaven', country='NZ')
        self.assertEqual(len(person.country), 2)

        person = Person(name='The Outsider', country=None)
        self.assertEqual(len(person.country), 0)
