from typing import Any, Dict, Union

from rest_framework import serializers
from django.utils.encoding import force_str

from django_countries import CountryCode, countries


class CountryField(serializers.ChoiceField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.country_dict = kwargs.pop("country_dict", None)
        self.name_only = kwargs.pop("name_only", None)
        field_countries = kwargs.pop("countries", None)
        self.countries = field_countries if field_countries else countries
        super().__init__(self.countries, *args, **kwargs)

    def to_representation(self, obj: CountryCode) -> Union[Dict[str, str], str]:
        code = self.countries.alpha2(obj)
        if not code:
            return ""
        if self.name_only:
            return force_str(self.countries.name(obj))
        if not self.country_dict:
            return code
        return {"code": code, "name": force_str(self.countries.name(obj))}

    def to_internal_value(self, data: Any) -> str:
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
