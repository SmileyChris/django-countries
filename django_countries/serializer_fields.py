from rest_framework import serializers
from django.utils.encoding import force_str

from django_countries import countries


class CountryField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.country_dict = kwargs.pop("country_dict", None)
        self.multiple = kwargs.pop("multiple", False)
        field_countries = kwargs.pop("countries", None)
        self.countries = field_countries if field_countries else countries
        super().__init__(self.countries, *args, **kwargs)

    def to_representation(self, obj):
        if self.multiple:
            country_list = []
            for key, code in enumerate(obj):
                country_list.append(
                    {
                        'code': self.countries.alpha2(obj[key]),
                        'name': self.countries.name(obj[key]),
                        'alpha3': self.countries.alpha3(obj[key]),
                    }
                )
        else:
            code = self.countries.alpha2(obj)
            if not code:
                return ""
            if not self.country_dict:
                return code
            country_list = {
                "code": code,
                "name": force_str(self.countries.name(obj)),
                "alpha3": force_str(self.countries.alpha3(obj))
            }

        return country_list

    def to_internal_value(self, data):
        if not self.allow_blank and data == "":
            self.fail("invalid_choice", input=data)

        if isinstance(data, dict):
            data = data.get("code")
        country = self.countries.alpha2(data)
        if data and not country:
            country = self.countries.by_name(force_str(data))
            if not country:
                self.fail("invalid_choice", input=data)
        return country
