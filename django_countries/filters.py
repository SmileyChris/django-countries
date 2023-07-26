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
        return [self.field_path]

    def choices(self, changelist):
        value = self.used_parameters.get(self.field_path)
        yield {
            "selected": value is None,
            "query_string": changelist.get_query_string({}, [self.field_path]),
            "display": _("All"),
        }
        for lookup, title in self.lookup_choices(changelist):
            yield {
                "selected": value == force_str(lookup),
                "query_string": changelist.get_query_string(
                    {self.field_path: lookup}, []
                ),
                "display": title,
            }

    def lookup_choices(self, changelist):
        qs = changelist.model._default_manager.all()
        codes = set(
            qs.distinct()
            .order_by(self.field_path)
            .values_list(self.field_path, flat=True)
        )
        for k, v in self.field.get_choices(include_blank=False):
            if k in codes:
                yield k, v
