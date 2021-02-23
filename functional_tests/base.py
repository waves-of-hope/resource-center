from pathlib import WindowsPath
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

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

        # get the user model
        cls.User = get_user_model()

    def tearDown(self):
        self.browser.quit()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        utils.test.tear_down_test_files()

    def get_absolute_file_path(self, relative_file_path):
        """Returns the absolute file path of files in the
        `test_files` directory as a string
        """
        try:
            absolute_path = settings.TEST_FILES_DIR.joinpath(
                relative_file_path)
            absolute_path_string = str(absolute_path.as_posix())

            if absolute_path.exists():
                if isinstance(absolute_path, WindowsPath):
                    return absolute_path_string.replace('/', '\\')
                return absolute_path_string
            else:
                raise ValueError(f"'{absolute_path_string}' does not exist")
        except TypeError as e:
            print('TypeError: {}'.format(e))

    def explicit_wait(self, test_method, max_wait_time=10):
        start_time = time.time()
        while True:
            try:
                return test_method
            except (WebDriverException) as e:
                if time.time() - start_time > max_wait_time:
                    raise e
                time.sleep(0.5)
