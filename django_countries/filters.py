from django.contrib import admin
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _


class CountryFilter(admin.FieldListFilter):
    """
    A country filter for Django admin that only returns a list of countries
    related to the model.
    """
    title = _('Country')

    def expected_parameters(self):
        return [self.field.name]

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(
                {}, [self.field.name]),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices(changelist):
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': changelist.get_query_string(
                    {self.field.name: lookup}, []),
                'display': title,
            }

    def lookup_choices(self, changelist):
        codes = changelist.queryset.values_list(self.field.name, flat=True)
        for k, v in self.field.get_choices(include_blank=False):
            if k in codes:
                yield k, v
