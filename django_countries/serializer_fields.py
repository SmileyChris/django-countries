from __future__ import unicode_literals

from rest_framework import serializers
from django.utils.encoding import force_text

from django_countries import countries


class CountryField(serializers.Field):

    def __init__(self, *args, **kwargs):
        self.country_dict = kwargs.pop('country_dict', None)
        countries_class = kwargs.pop('countries', None)
        self.countries = countries_class() if countries_class else countries
        super(CountryField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        code = self.countries.alpha2(obj)
        if not code:
            return ''
        if not self.country_dict:
            return code
        return {'code': code, 'name': force_text(self.countries.name(obj))}

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.get('code')
        return self.countries.alpha2(data)
