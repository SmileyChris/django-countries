from django.db import models
from django_countries import CountryField
from django_countries.tests.fields import TestCountryField


class Person(models.Model):
    name = models.CharField(max_length=50)
    country = CountryField(blank=True)
