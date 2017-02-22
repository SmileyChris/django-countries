from django.db import models
from django_countries.fields import CountryField
from django_countries.tests import custom_countries


class Person(models.Model):
    name = models.CharField(max_length=50)
    country = CountryField()
    other_country = CountryField(
        blank=True, countries_flag_url='//flags.example.com/{code}.gif')
    favourite_country = CountryField(default='NZ')
    fantasy_country = CountryField(
        countries=custom_countries.FantasyCountries, blank=True)

    class Meta:
        ordering = ('name',)


class AllowNull(models.Model):
    country = CountryField(null=True, blank_label='(select country)')


class MultiCountry(models.Model):
    countries = CountryField(multiple=True)
    uneditable_countries = CountryField(multiple=True, editable=False)
