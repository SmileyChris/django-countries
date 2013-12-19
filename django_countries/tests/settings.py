SECRET_KEY = 'test'

INSTALLED_APPS = (
    'django_countries',
    'django_countries.tests',
)

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3'}
}

STATIC_URL = '/static-assets/'
