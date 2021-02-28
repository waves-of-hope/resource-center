from pathlib import WindowsPath
from shutil import rmtree, copy
import time

from django.conf import settings

from selenium.common import exceptions


images = ['default.png', 'book-cover.png', 'book-cover.jpg']
documents = ['book.pdf']

def set_up_test_files():
    if settings.MEDIA_ROOT.exists():
        tear_down_test_files()

    settings.MEDIA_ROOT.mkdir()
    test_images_dir = settings.TEST_FILES_DIR.joinpath('images')
    test_docs_dir = settings.TEST_FILES_DIR.joinpath('documents')

    for image in images:
        copy(test_images_dir.joinpath(image), settings.MEDIA_ROOT)

    for doc in documents:
        copy(test_docs_dir.joinpath(doc), settings.MEDIA_ROOT)

    return test_images_dir, test_docs_dir

def tear_down_test_files():
    rmtree(settings.MEDIA_ROOT)

def get_absolute_file_path(relative_file_path):
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

def explicit_wait(test_method, max_wait_time=10):
    start_time = time.time()
    while True:
        try:
            return test_method
        except (
            exceptions.WebDriverException,
            exceptions.NoSuchElementException
        ) as e:
            if time.time() - start_time > max_wait_time:
                raise e
            time.sleep(0.5)
