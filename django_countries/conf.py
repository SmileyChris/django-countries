import django.conf


class AppSettings(django.conf.BaseSettings):
    """
    A holder for app-specific default settings that allows overriding via
    the project's settings.
    """

    def __getattribute__(self, attr):
        if attr == attr.upper():
            try:
                return getattr(django.conf.settings, attr)
            except AttributeError:
                pass
        return super(AppSettings, self).__getattribute__(attr)


class Settings(AppSettings):
    COUNTRIES_FLAG_URL = 'flags/{code}.gif'
    """
    The URL for a flag.

    It can either be relative to the static url, or an absolute url.

    The location is parsed using Python's string formatting and is passed the
    following arguments:

        * code
        * code_upper

    For example: ``COUNTRIES_FLAG_URL = 'flags/16x10/{code_upper}.png'``
    """

    COUNTRIES_COMMON_NAMES = True
    """
    Whether to use the common names for some countries, as opposed to the
    official ISO name.

    Some examples:
        "Bolivia" instead of "Bolivia, Plurinational State of"
        "South Korea" instead of "Korea (the Republic of)"
        "Taiwan" instead of "Taiwan (Province of China)"
    """

    COUNTRIES_OVERRIDE = {}
    """
    A dictionary of names to override the defaults.

    Note that you will need to handle translation of customised country names.

    Setting a country's name to ``None`` will exclude it from the country list.
    For example::

        COUNTRIES_OVERRIDE = {
            'NZ': _('Middle Earth'),
            'AU': None
        }
    """

    COUNTRIES_ONLY = {}
    """
    Similar to COUNTRIES_OVERRIDE
    A dictionary of names to include in selection.

    Note that you will need to handle translation of customised country names.

    For example::

        COUNTRIES_ONLY = {
            'NZ': _('Middle Earth'),
            'AU': _('Desert'),
        }
    """

settings = Settings()
