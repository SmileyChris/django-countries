from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class CountryFilter(admin.SimpleListFilter):
    """
    A country filter for Django admin that only returns a list of countries related to the model.
    """
    title = _('Country')
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        return set([
            (obj.country, obj.country.name) for obj in model_admin.model.objects.exclude(
                country__isnull=True
            ).exclude(country__exact='')
        ])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country=self.value())
        else:
            return queryset

