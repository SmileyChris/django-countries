from django.conf import settings


def _build_flag_url():
    if hasattr(settings, 'COUNTRIES_FLAG_URL'):
        url = settings.COUNTRIES_FLAG_URL
    else:
        url = 'flags/%(code)s.gif'
    prefix = getattr(settings, 'STATIC_URL', '') or settings.MEDIA_URL
    if not prefix.endswith('/'):
        prefix = '%s/' % prefix
    return '%s%s' % (prefix, url)


FLAG_URL = _build_flag_url()
