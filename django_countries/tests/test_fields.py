# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
from django.forms import Select
from django.forms.models import modelform_factory
from django.test import TestCase
from django.utils import translation
from django.utils.encoding import force_text
try:
    from unittest import skipIf
except:
    from django.utils.unittest import skipIf

from django_countries import fields, countries
from django_countries.tests import forms, custom_countries
from django_countries.tests.models import Person, AllowNull, en_zed

skipUnlessLegacy = skipIf(
    django.VERSION >= (1, 5),
    "Legacy tests only necessary in Django < 1.5")


class TestCountryField(TestCase):

    def test_logic(self):
        person = Person(name='Chris Beaven', country='NZ')

        self.assertEqual(person.country, 'NZ')
        self.assertNotEqual(person.country, 'ZZ')

        self.assertTrue(person.country)
        person.country = ''
        self.assertFalse(person.country)

    def test_only_from_instance(self):
        self.assertRaises(AttributeError, lambda: Person.country)

    @skipIf(
        django.VERSION < (1, 7), "Field.deconstruct introduced in Django 1.7")
    def test_deconstruct(self):
        field = Person._meta.get_field('country')
        self.assertEqual(
            field.deconstruct(),
            ('country', 'django_countries.fields.CountryField', [],
             {'max_length': 2}))

    def test_text(self):
        person = Person(name='Chris Beaven', country='NZ')
        self.assertEqual(force_text(person.country), 'NZ')

    def test_name(self):
        person = Person(name='Chris Beaven', country='NZ')
        self.assertEqual(person.country.name, 'New Zealand')

    def test_flag(self):
        person = Person(name='Chris Beaven', country='NZ')
        with self.settings(STATIC_URL='/static-assets/'):
            self.assertEqual(
                person.country.flag, '/static-assets/flags/nz.gif')

    def test_custom_field_flag_url(self):
        person = Person(name='Chris Beaven', country='NZ', other_country='US')
        self.assertEqual(
            person.other_country.flag, '//flags.example.com/us.gif')

    def test_COUNTRIES_FLAG_URL_setting(self):
        # Custom relative url
        person = Person(name='Chris Beaven', country='NZ')
        with self.settings(COUNTRIES_FLAG_URL='img/flag-{code_upper}.png',
                           STATIC_URL='/static-assets/'):
            self.assertEqual(
                person.country.flag, '/static-assets/img/flag-NZ.png')
        # Custom absolute url
        with self.settings(COUNTRIES_FLAG_URL='https://flags.example.com/'
                           '{code_upper}.PNG'):
            self.assertEqual(
                person.country.flag, 'https://flags.example.com/NZ.PNG')

    def test_blank(self):
        person = Person.objects.create(name='The Outsider')
        self.assertEqual(person.country, '')

        person = Person.objects.get(pk=person.pk)
        self.assertEqual(person.country, '')

    def test_null(self):
        person = AllowNull.objects.create(country=None)
        self.assertIsNone(person.country.code)

        person = AllowNull.objects.get(pk=person.pk)
        self.assertIsNone(person.country.code)

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
        Person.objects.create(name='The Outsider')
        person = Person.objects.get()
        self.assertEqual(person.country, '')

    def test_create_modelform(self):
        Form = modelform_factory(Person, fields=['country'])
        form_field = Form().fields['country']
        self.assertTrue(isinstance(form_field.widget, Select))

    def test_render_form(self):
        Form = modelform_factory(Person, fields=['country'])
        Form().as_p()

    def test_custom_country(self):
        self.assertEqual(
            list(Person._meta.get_field('fantasy_countries').choices),
            [('NV', 'Neverland'), ('NZ', 'New Zealand')])

    @skipIf(
        django.VERSION < (1, 7), "Field.deconstruct introduced in Django 1.7")
    def test_custom_country_deconstruct(self):
        field = Person._meta.get_field('fantasy_countries')
        self.assertEqual(
            field.deconstruct(),
            (
                'fantasy_countries',
                'django_countries.fields.CountryField',
                [],
                {
                    'countries': custom_countries.FantasyCountries,
                    'max_length': 2
                }
            ))


class TestCountryObject(TestCase):

    def test_hash(self):
        country = fields.Country(code='XX', flag_url='')
        self.assertEqual(hash(country), hash('XX'))

    def test_repr(self):
        country1 = fields.Country(code='XX')
        country2 = fields.Country(code='XX', flag_url='')
        self.assertEqual(
            repr(country1),
            'Country(code={0})'.format(repr('XX')))
        self.assertEqual(
            repr(country2),
            'Country(code={0}, flag_url={1})'.format(repr('XX'), repr('')))

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

    def test_alpha3(self):
        country = fields.Country(code='BN')
        self.assertEqual(country.alpha3, 'BRN')

    def test_alpha3_invalid(self):
        country = fields.Country(code='XX')
        self.assertEqual(country.alpha3, '')

    def test_numeric(self):
        country = fields.Country(code='BN')
        self.assertEqual(country.numeric, 96)

    def test_numeric_padded(self):
        country = fields.Country(code='AL')
        self.assertEqual(country.numeric_padded, '008')
        country = fields.Country(code='BN')
        self.assertEqual(country.numeric_padded, '096')
        country = fields.Country(code='NZ')
        self.assertEqual(country.numeric_padded, '554')

    def test_numeric_invalid(self):
        country = fields.Country(code='XX')
        self.assertEqual(country.numeric, None)

    def test_numeric_padded_invalid(self):
        country = fields.Country(code='XX')
        self.assertEqual(country.numeric_padded, None)


class TestModelForm(TestCase):

    def test_translated_choices(self):
        lang = translation.get_language()
        translation.activate('eo')
        form = forms.PersonForm()
        try:
            # This is just to prove that the language changed.
            self.assertEqual(list(countries)[0][1], 'Afganio')
            # If the choices aren't lazy, this wouldn't be translated. It's the
            # second choice because the first one is the initial blank option.
            self.assertEqual(
                form.fields['country'].choices[1][1], 'Afganio')
            self.assertEqual(
                form.fields['country'].widget.choices[1][1], 'Afganio')
        finally:
            translation.activate(lang)

    def test_blank_choice(self):
        form = forms.PersonForm()
        self.assertEqual(form.fields['country'].choices[0], ('', '---------'))

    def test_no_blank_choice(self):
        form = forms.PersonForm()
        self.assertEqual(
            form.fields['favourite_country'].choices[0], ('AF', 'Afghanistan'))

    def test_blank_choice_label(self):
        form = forms.AllowNullForm()
        self.assertEqual(
            form.fields['country'].choices[0], ('', '(select country)'))

    @skipUnlessLegacy
    def test_legacy_default(self):
        self.assertEqual(
            forms.LegacyForm.base_fields['default'].initial, 'AU')

    @skipUnlessLegacy
    def test_legacy_default_callable(self):
        self.assertEqual(
            forms.LegacyForm.base_fields['default_callable'].initial, en_zed)
        form = forms.LegacyForm()
        self.assertEqual(form['default_callable'].value(), 'NZ')

    @skipUnlessLegacy
    def test_legacy_empty_value(self):
        self.assertEqual(
            forms.LegacyForm.base_fields['default'].empty_value, None)
        self.assertEqual(
            forms.LegacyForm.base_fields['default_callable'].empty_value, '')
