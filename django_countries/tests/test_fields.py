from __future__ import unicode_literals
from django.test import TestCase
from django.utils.encoding import force_text

from django_countries import fields
from django_countries.tests.models import Person, AllowNull


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

    def test_lookup_text(self):
        Person.objects.create(name='Chris Beaven', country='NZ')
        Person.objects.create(name='Pavlova', country='NZ')
        Person.objects.create(name='Killer everything', country='AU')

        lookup = Person.objects.filter(country='NZ')
        names = lookup.order_by('name').values_list('name', flat=True)
        self.assertEqual(list(names), ['Chris Beaven', 'Pavlova'])

    def test_lookup_country(self):
        Person.objects.create(name='Chris Beaven', country='NZ')
        Person.objects.create(name='Pavlova', country='NZ')
        Person.objects.create(name='Killer everything', country='AU')

        oz = fields.Country(code='AU', flag_url='')
        lookup = Person.objects.filter(country=oz)
        names = lookup.values_list('name', flat=True)
        self.assertEqual(list(names), ['Killer everything'])

    def test_save_empty_country(self):
        Person.objects.create(name='The Outsider', country=None)
        AllowNull.objects.create(country=None)


class TestCountryObject(TestCase):

    def test_hash(self):
        country = fields.Country(code='XX', flag_url='')
        self.assertEqual(hash(country), hash('XX'))

    def test_repr(self):
        country = fields.Country(code='XX', flag_url='')
        self.assertEqual(
            repr(country),
            'Country(code={}, flag_url={})'.format(repr('XX'), repr('')))

    def test_flag_on_empty_code(self):
        country = fields.Country(code='', flag_url='')
        self.assertEqual(country.flag, '')

    def test_ioc_code(self):
        country = fields.Country(code='NL', flag_url='')
        self.assertEqual(country.ioc_code, 'NED')

    def test_country_from_ioc_code(self):
        country = fields.Country.country_from_ioc('NED')
        self.assertEqual(country, fields.Country('NL', flag_url=''))

    def test_country_from_blank_ioc_code(self):
        country = fields.Country.country_from_ioc('')
        self.assertIsNone(country)

    def test_country_from_nonexistence_ioc_code(self):
        country = fields.Country.country_from_ioc('XXX')
        self.assertIsNone(country)
