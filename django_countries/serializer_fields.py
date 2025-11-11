from typing import Any

from django.utils.encoding import force_str
from rest_framework import serializers

from django_countries import countries


class CountryField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.country_dict = kwargs.pop("country_dict", None)
        self.name_only = kwargs.pop("name_only", None)
        field_countries = kwargs.pop("countries", None)
        self.countries = field_countries or countries
        super().__init__(
            self.countries,  # type: ignore
            *args,
            **kwargs,
        )
        # Set up drf-spectacular annotation
        self._setup_spectacular_annotation()

    def to_representation(self, obj):
        code = self.countries.alpha2(obj)
        if not code:
            # Respect allow_null setting for empty values
            if self.allow_null:
                return None
            return ""
        if self.name_only:
            return force_str(self.countries.name(obj))
        if not self.country_dict:
            return code
        return {"code": code, "name": force_str(self.countries.name(obj))}

    def to_internal_value(self, data: Any):
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

    def _get_country_dict_schema(self):
        """Return schema for country_dict representation."""
        schema = {
            "type": "object",
            "properties": {
                "code": {"type": "string", "minLength": 2, "maxLength": 2},
                "name": {"type": "string"},
            },
            "required": ["code", "name"],
        }
        if self.allow_null:
            schema = {"oneOf": [schema, {"type": "null"}]}
        return schema

    def _get_name_only_schema(self):
        """Return schema for name_only representation."""
        schema = {"type": "string"}
        if self.allow_null:
            schema = {"oneOf": [schema, {"type": "null"}]}
        return schema

    def _setup_spectacular_annotation(self):
        """
        Set up schema annotation for drf-spectacular.

        This sets the _spectacular_annotation attribute that drf-spectacular
        checks when generating OpenAPI schemas. When country_dict=True or
        name_only=True, we override the default ChoiceField enum schema
        with the appropriate schema for the actual representation.
        """
        if self.country_dict:
            schema = self._get_country_dict_schema()
            # Store as 'field' key like extend_schema_field decorator does
            self._spectacular_annotation = {"field": schema}
        elif self.name_only:
            schema = self._get_name_only_schema()
            self._spectacular_annotation = {"field": schema}
        # For standard code output, don't set annotation to allow
        # default ChoiceField enum handling
