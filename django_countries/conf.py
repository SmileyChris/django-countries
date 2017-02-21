import django.conf


class AppSettings(object):
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

    COUNTRIES_FIRST = []
    """
    Countries matching the country codes provided in this list will be shown
    first in the countries list (in the order specified) before all the
    alphanumerically sorted countries.
    """

    COUNTRIES_FIRST_REPEAT = False
    """
    Countries listed in :attr:`COUNTRIES_FIRST` will be repeated again in the
    alphanumerically sorted list if set to ``True``.
    """

    COUNTRIES_FIRST_BREAK = None
    """
    Countries listed in :attr:`COUNTRIES_FIRST` will be followed by a null
    choice with this title (if set) before all the alphanumerically sorted
    countries.
    """

    COUNTRIES_FIRST_SORT = False
    """
    Countries listed in :attr:`COUNTRIES_FIRST` will be alphanumerically
    sorted based on their translated name instead of relying on their
    order in :attr:`COUNTRIES_FIRST`.
    """

    COUNTRIES_USE_REGIONS = False
    """
    If set to ``False`` regions will not be initiated automatically. If you set
    the regions attribute of the Countries object explicitly, this setting is ignored.

    Note that other region settings are ignored when this is set to False.
    """

    COUNTRIES_REGION_ONLY = []
    """
    Only countries located in this list of (UN M.49) geographical region codes
    will  be included in the selection
    """

    REGIONS_OVERRIDE = {}
    """
    A dictionary of names to override the default UN M.49 geographical region names

    Note that you will need to handle translation of customised region names.

    Setting a region's name to ``None`` will exclude it from the country list.

    For example::

        REGIONS_OVERRIDE = {
            1: _('3rd Rock from the Sun'),
            53: None
        }
    """

    REGIONS_ONLY = {}
    """
    A dictionary of names to include as region names

    Note that you will need to handle translation of customised region names.

    Also note that you will probably have to set :attr:`REGIONS_MAP_OVERRIDE`
    as well when you use this setting

    For example::

        REGIONS_ONLY = {
            900:_("ITU World"),
            901: _("ITU Region 1"),
            902: _("ITU Region 2"),
            903: _("ITU Region 3"),
        }
    """

    REGIONS_MAP_ONLY_LOOKUP = False
    """
    If set to ``True`` the values of the new listed region map in :attr:`REGIONS_MAP_ONLY`
    will be looked up from the default UN M.49 list and be replaced with the list of
    countries region code that are located in those regions

    Note that you probably can not use this feature if any of your region codes are
    already used for a M.49 region (you can get circular references). It is advised that when you use this feature
    you use the region codes 900 to 999 which are reserved for
    private use (both in UN M.49 as ISO 3166-1)

    You can exclude specific regions/coutries by prefixing the region code with a !
    """

    REGIONS_MAP_ONLY = {}
    """
    A dictionary of region lists to override the default UN M.49 regions

    Note that you have to make sure that your map has no circular references which can
    cause recursion loops. Region codes should always be an integer

    For example::
        REGIONS_MAP_ONLY_LOOKUP = True

        REGIONS_MAP_ONLY = {
            900: [901, 901, 903],
            901: [2, 143, 145, 150, 496],
            902: [19],
            903: [9, 30, 34, 35, "!496"],
        }
    """

settings = Settings()
