from django.db import models
from django_countries.fields import CountryField
from django_countries.tests import custom_countries


def en_zed():
    return 'NZ'


class Person(models.Model):
    name = models.CharField(max_length=50)
    country = CountryField()
    other_country = CountryField(
        blank=True, countries_flag_url='//flags.example.com/{code}.gif')
    favourite_country = CountryField(default='NZ')
    fantasy_countries = CountryField(
        countries=custom_countries.FantasyCountries)


class AllowNull(models.Model):
    country = CountryField(null=True, blank_label='(select country)')


class Legacy(models.Model):
    default = CountryField(default='AU', null=True)
    default_callable = CountryField(default=en_zed)
