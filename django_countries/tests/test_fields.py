from __future__ import unicode_literals
from django.test import TestCase
from django_countries.tests.models import Person
from django.utils.encoding import force_text


class TestCountryField(TestCase):

    def test_logic(self):
        person = Person(name='Chris Beaven', country='NZ')

        self.assertEqual(person.country, 'NZ')
        self.assertNotEqual(person.country, 'ZZ')

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
        self.assertEqual(person.country.flag, '/static-assets/flags/nz.gif')

    def test_custom_field_flag_url(self):
        person = Person(name='Chris Beaven', country='NZ', other_country='US')
        self.assertEqual(
            person.other_country.flag, '//flags.example.com/us.gif')

    def test_COUNTRIES_FLAG_URL_setting(self):
        # Custom relative url
        person = Person(name='Chris Beaven', country='NZ')
        with self.settings(COUNTRIES_FLAG_URL='img/flag-{code_upper}.png'):
            self.assertEqual(
                person.country.flag, '/static-assets/img/flag-NZ.png')
        # Custom absolute url
        with self.settings(COUNTRIES_FLAG_URL='https://flags.example.com/'
                           '{code_upper}.PNG'):
            self.assertEqual(
                person.country.flag, 'https://flags.example.com/NZ.PNG')

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
