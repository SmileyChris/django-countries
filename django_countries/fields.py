from __future__ import unicode_literals

from django.core.files.storage import default_storage
from django.db.models.fields import CharField
from django.utils.encoding import force_text, python_2_unicode_compatible

from django_countries import countries
from django_countries.conf import settings


@python_2_unicode_compatible
class Country(object):
    def __init__(self, code, storage):
        self.code = code
        self.storage = storage

    def __str__(self):
        return force_text(self.code or '')

    def __eq__(self, other):
        return force_text(self) == force_text(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(force_text(self))

    def __repr__(self):
        return "%s(code=%s)" % (self.__class__.__name__, self)

    def __bool__(self):
        return bool(self.code)

    __nonzero__ = __bool__   # Python 2 compatibility.

    def __len__(self):
        return len(force_text(self))

    @property
    def name(self):
        return countries.name(self.code)

    @property
    def flag(self):
        if not self.code:
            return ''
        path = settings.COUNTRIES_FLAG_STATIC.format(
            code_upper=self.code, code=self.code.lower())
        return self.storage.url(path)


class CountryDescriptor(object):
    """
    A descriptor for country fields on a model instance. Returns a Country when
    accessed so you can do things like::

        >>> from people import Person
        >>> person = Person.object.get(name='Chris')

        >>> person.country.name
        u'New Zealand'

        >>> person.country.flag
        '/static/flags/nz.gif'
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))
        return Country(
            code=instance.__dict__[self.field.name],
            storage=self.field.flag_storage)

    def __set__(self, instance, value):
        if value is not None:
            value = force_text(value)
        instance.__dict__[self.field.name] = value


class CountryField(CharField):
    """
    A country field for Django models that provides all ISO 3166-1 countries as
    choices.
    """
    descriptor_class = CountryDescriptor

    def __init__(self, *args, **kwargs):
        self.flag_storage = kwargs.pop('flag_storage', None) or default_storage
        super(CharField, self).__init__(
            max_length=2, choices=countries, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def contribute_to_class(self, cls, name):
        super(CountryField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def get_prep_lookup(self, lookup_type, value):
        if hasattr(value, 'code'):
            value = value.code
        return super(CountryField, self).get_prep_lookup(lookup_type, value)

    def pre_save(self, *args, **kwargs):
        "Returns field's value just before saving."
        value = super(CharField, self).pre_save(*args, **kwargs)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        # Convert the Country to unicode for database insertion.
        if value is None:
            return None
        return force_text(value)


# If south is installed, ensure that CountryField will be introspected just
# like a normal CharField.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django_countries\.fields\.CountryField'])
except ImportError:
    pass
