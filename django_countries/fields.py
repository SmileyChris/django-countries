from __future__ import unicode_literals

try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse   # Python 2

from django import forms
from django.db.models.fields import CharField
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.functional import lazy, Promise

from django_countries import countries, ioc_data
from django_countries.conf import settings


@python_2_unicode_compatible
class Country(object):
    def __init__(self, code, flag_url=None):
        self.code = code
        self.flag_url = flag_url

    def __str__(self):
        if not self.code:
            return ''
        return force_text(self.code)

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(force_text(self))

    def __repr__(self):
        if self.flag_url is None:
            repr_text = "{0}(code={1})"
        else:
            repr_text = "{0}(code={1}, flag_url={2})"
        return repr_text.format(
            self.__class__.__name__, repr(self.code), repr(self.flag_url))

    def __bool__(self):
        return bool(self.code)

    __nonzero__ = __bool__   # Python 2 compatibility.

    def __len__(self):
        return len(force_text(self))

    @property
    def name(self):
        return countries.name(self.code)

    @property
    def alpha3(self):
        return countries.alpha3(self.code)

    @property
    def numeric(self):
        return countries.numeric(self.code)

    @property
    def numeric_padded(self):
        return countries.numeric(self.code, padded=True)

    @property
    def flag(self):
        flag_url = self.flag_url
        if flag_url is None:
            flag_url = settings.COUNTRIES_FLAG_URL
        url = flag_url.format(
            code_upper=self.code, code=self.code.lower())
        return urlparse.urljoin(settings.STATIC_URL, url)

    @staticmethod
    def country_from_ioc(ioc_code, flag_url=''):
        code = ioc_data.IOC_TO_ISO.get(ioc_code, '')
        if code == '':
            return None
        return Country(code, flag_url=flag_url)

    @property
    def ioc_code(self):
        return ioc_data.ISO_TO_IOC.get(self.code, '')


class CountryDescriptor(object):
    """
    A descriptor for country fields on a model instance. Returns a Country when
    accessed so you can do things like::

        >>> from people import Person
        >>> person = Person.object.get(name='Chris')

        >>> person.country.name
        'New Zealand'

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
        code = instance.__dict__[self.field.name]
        if not code:
            return Country(code=code)
        return Country(
            code=code,
            flag_url=self.field.countries_flag_url,
        )

    def __set__(self, instance, value):
        if value is not None:
            value = force_text(value)
        instance.__dict__[self.field.name] = value


class LazyTypedChoiceField(forms.TypedChoiceField):
    """
    A form TypedChoiceField that respects choices being a lazy object.
    """

    @property
    def choices(self):
        """
        When it's time to get the choices, if it was a lazy then figure it out
        now and memoize the result.
        """
        if isinstance(self._choices, Promise):
            self._choices = list(self._choices)
        return self._choices

    @choices.setter
    def choices(self, value):
        self._choices = value


class CountryField(CharField):
    """
    A country field for Django models that provides all ISO 3166-1 countries as
    choices.
    """
    descriptor_class = CountryDescriptor

    def __init__(self, *args, **kwargs):
        self.countries_flag_url = kwargs.pop('countries_flag_url', None)
        kwargs.update({
            'max_length': 2,
            'choices': countries,
        })
        super(CharField, self).__init__(*args, **kwargs)

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
        if hasattr(value, 'code'):
            value = value.code
        return super(CountryField, self).get_prep_value(value)

    def deconstruct(self):
        """
        Remove choices from deconstructed field, as this is the country list
        and not user editable.
        """
        name, path, args, kwargs = super(CountryField, self).deconstruct()
        kwargs.pop('choices')
        return name, path, args, kwargs

    get_choices = lazy(CharField.get_choices, list)

    def formfield(self, **kwargs):
        argname = 'choices_form_class'
        if argname not in kwargs:
            kwargs[argname] = LazyTypedChoiceField
        # if not 'widget' in kwargs:
        #     kwargs['widget'] = CountrySelectWidget()
        field = super(CharField, self).formfield(**kwargs)
        if not isinstance(field, LazyTypedChoiceField):
            field = self.legacy_formfield(**kwargs)
        return field

    def legacy_formfield(self, **kwargs):
        """
        Legacy method to fix Django LTS not allowing a custom choices form
        class.
        """
        from django.utils.text import capfirst

        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()
        include_blank = (self.blank or
                         not (self.has_default() or 'initial' in kwargs))
        defaults['choices'] = self.get_choices(include_blank=include_blank)
        defaults['coerce'] = self.to_python
        if self.null:
            defaults['empty_value'] = None
        form_class = LazyTypedChoiceField
        # Many of the subclass-specific formfield arguments (min_value,
        # max_value) don't apply for choice fields, so be sure to only pass
        # the values that TypedChoiceField will understand.
        for k in kwargs.keys():
            if k not in ('coerce', 'empty_value', 'choices', 'required',
                         'widget', 'label', 'initial', 'help_text',
                         'error_messages', 'show_hidden_initial'):
                del kwargs[k]
        defaults.update(kwargs)
        return form_class(**defaults)


# If south is installed, ensure that CountryField will be introspected just
# like a normal CharField.
try:  # pragma: no cover
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django_countries\.fields\.CountryField'])
except ImportError:
    pass
