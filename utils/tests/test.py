import time
import unittest

from django.conf import settings

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import utils.test


class TestUtilsTestCase(unittest.TestCase):

    def test_set_up_test_files(self):
        test_images, test_docs = utils.test.set_up_test_files()

        images_absolute_file_path = [path.name for path in test_images.iterdir()]
        for image in utils.test.images:
            self.assertIn(image, images_absolute_file_path)

        docs_absolute_file_paths = [path.name for path in test_docs.iterdir()]
        for doc in utils.test.documents:
            self.assertIn(doc, docs_absolute_file_paths)

    def test_tear_down_test_files(self):
        utils.test.set_up_test_files()
        utils.test.tear_down_test_files()
        self.assertFalse(settings.MEDIA_ROOT.exists())

    def test_get_absolute_file_path(self):
        with self.assertRaises(TypeError):
            utils.test.get_absolute_file_path()

        with self.assertRaises(ValueError):
            utils.test.get_absolute_file_path('does-not-exist')

        test_file = 'images/' + utils.test.images[0]
        test_files_paths = [
            str(path) for path in settings.TEST_FILES_DIR.rglob('*')
        ]
        self.assertIn(
            utils.test.get_absolute_file_path(test_file),
            test_files_paths
        )

    def test_explicit_wait(self):
        self.browser_options = webdriver.firefox.options.Options()
        self.browser_options.headless = settings.HEADLESS_BROWSER_TESTS
        self.browser = webdriver.Firefox(options=self.browser_options)
        self.browser.get('http://google.com/')
        
        start_time = time.time()
        with self.assertRaises(WebDriverException):
            utils.test.explicit_wait(
                self.assertEqual(
                    self.browser.find_element_by_name('Does not exist')
                )
            )
        end_time = time.time()

        self.assertGreaterEqual(20, end_time - start_time)

        self.browser.quit()


if __name__ == '_main__':
    unittest.main()
