import os
import time
import warnings

from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.test.runner import DiscoverRunner
from django.test.utils import override_settings

from channel2.account.models import User

MEDIA_ROOT_TEST = os.path.join(settings.BASE_DIR, 'media-test')


class Channel2TestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        db = super().setup_databases(**kwargs)
        call_command('datacreator')
        return db

    def teardown_databases(self, old_config, **kwargs):
        super().teardown_databases(old_config, **kwargs)


def fast_set_password(self, raw_password):
    self.password = raw_password


def fast_check_password(self, raw_password):
    return self.password == raw_password


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class BaseTestCase(TestCase):

    # Number of milliseconds a test can take before it is considered "too long".
    DURATION_THRESHOLD = 150

    def setUp(self):
        super().setUp()
        cache.clear()

        # Override setting and checking of password for speed.
        User.set_password = fast_set_password
        User.check_password = fast_check_password

        # Login with the testuser@example.com.
        self.user = User.objects.get(email='testuser@example.com')
        self.client.login(email=self.user.email, password=self.user.password)
        self.test_start = time.time()

    def tearDown(self):
        duration = self.get_test_duration()
        if duration > self.DURATION_THRESHOLD:
            message = '{} is slower than {}ms: {}ms.'.format(
                self._testMethodName, self.DURATION_THRESHOLD, duration)
            warnings.warn(message)
        super().tearDown()

    def get_test_duration(self):
        return int((time.time() - self.test_start) * 1000)

    def assertTemplateUsed(self, response, template_name):
        self.assertEqual(response.template_name, template_name)
