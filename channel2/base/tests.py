import time
import warnings

from django.core.cache import cache
from django.test import TestCase
from django.test.runner import DiscoverRunner


class Channel2TestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        return super().setup_databases(**kwargs)


class BaseTestCase(TestCase):

    # Number of milliseconds a test can take before it is considered "too long".
    DURATION_THRESHOLD = 150

    def setUp(self):
        super().setUp()
        self.test_start = time.time()
        cache.clear()

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
