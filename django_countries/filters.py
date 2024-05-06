import django
from django.contrib import admin
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class CountryFilter(admin.FieldListFilter):
    """
    A country filter for Django admin that only returns a list of countries
    related to the model.
    """

    title = _("Country")  # type: ignore

    def expected_parameters(self):
        if self.field.multiple:
            return [f"{self.field.name}__contains"]
        return [self.field.name]

    def choices(self, changelist):
        if self.field.multiple:
            field_name = f"{self.field.name}__contains"
        else:
            field_name = self.field.name

        value = self.used_parameters.get(field_name)
        yield {
            "selected": value is None,
            "query_string": changelist.get_query_string({}, [field_name]),
            "display": _("All"),
        }
        for lookup, title in self.lookup_choices(changelist):
            if django.VERSION >= (5, 0):
                selected = value is not None and force_str(lookup) in value
            else:
                selected = force_str(lookup) == value
            yield {
                "selected": selected,
                "query_string": changelist.get_query_string({field_name: lookup}, []),
                "display": title,
            }

    def lookup_choices(self, changelist):
        qs = changelist.model._default_manager.all()
        codes = set(
            ",".join(
                qs.distinct()
                .order_by(self.field.name)
                .values_list(self.field.name, flat=True)
            ).split(",")
        )
        for k, v in self.field.get_choices(include_blank=False):
            if k in codes:
                yield k, v
