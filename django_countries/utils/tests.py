from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.db.models.loading import load_app


class TempAppTestCase(TestCase):
    """
    A Django test case which also handles test-only applications.

    """
    test_apps = ()

    def setUp(self):
        self.old_INSTALLED_APPS = settings.INSTALLED_APPS
        settings.INSTALLED_APPS = (tuple(settings.INSTALLED_APPS) +
                                   self.test_apps)
        for app in self.test_apps:
            load_app(app)
        if self.test_apps:
            # Create tables for any test-only applications.
            call_command('syncdb', verbosity=0, interactive=False)

    def tearDown(self):
        settings.INSTALLED_APPS = self.old_INSTALLED_APPS  
