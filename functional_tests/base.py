from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium import webdriver

import utils.test


@tag('functional')
class ResourceCenterTestCase(StaticLiveServerTestCase):
    """Sets up data to be shared across Resource Center functional tests

    Args:
        StaticLiveServerTestCase (object): A subclass of
        django.test.LiveServerTestCase
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        utils.test.set_up_test_files()

        # set browser options based on settings
        cls.browser_options = webdriver.firefox.options.Options()
        cls.browser_options.headless = settings.HEADLESS_BROWSER_TESTS

        cls.User = get_user_model()

    def get_admin_url(self):
        """Returns the admin URL from the `ADMIN_URL` configuration

        Returns:
            string: The link to the homepage of the admin site
        """
        return f'{self.live_server_url}/{settings.ADMIN_URL}/'

    def tearDown(self):
        self.browser.quit()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        utils.test.tear_down_test_files()
