from pathlib import WindowsPath
from shutil import rmtree, copy

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag

from selenium import webdriver


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

        # set browser options based on settings
        cls.browser_options = webdriver.firefox.options.Options()
        cls.browser_options.headless = settings.HEADLESS_BROWSER_TESTS

        # get the user model
        cls.User = get_user_model()

        # set up test media directory
        settings.MEDIA_ROOT.mkdir()
        test_images = settings.TEST_FILES_DIR / 'images'
        copy(test_images.joinpath('default.png'), settings.MEDIA_ROOT)
        copy(test_images.joinpath('book-cover.png'), settings.MEDIA_ROOT)
        copy(test_images.joinpath('book-cover.jpg'), settings.MEDIA_ROOT)
        copy(
            settings.TEST_FILES_DIR.joinpath('documents/book.pdf'),
            settings.MEDIA_ROOT
        )

    def tearDown(self):
        self.browser.quit()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # remove test media directory
        rmtree(settings.MEDIA_ROOT)

    def get_abs_test_file_path(self, rel_file_path):
        """Returns the absolute file path of files in the
        `test_files` directory as a string
        """
        try:
            abs_path = settings.TEST_FILES_DIR.joinpath(rel_file_path)
            abs_path_str = str(abs_path.as_posix())
        except TypeError as e:
            print('TypeError: {}'.format(e))

        if abs_path.exists():
            if isinstance(abs_path, WindowsPath):
                return abs_path_str.replace('/', '\\')
            return abs_path_str
        else:
            raise ValueError("'{}' does not exist".\
                format(abs_path_str))
