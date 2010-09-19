from django.db import models
from django_countries import CountryField


class Person(models.Model):
    name = models.CharField(max_length=50)
    country = CountryField(blank=True)
