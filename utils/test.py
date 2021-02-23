from shutil import rmtree, copy

from django.conf import settings


images = ['default.png', 'book-cover.png', 'book-cover.jpg']
documents = ['book.pdf']

def set_up_test_files():
    settings.MEDIA_ROOT.mkdir()
    for image in images:
        copy(
            settings.TEST_FILES_DIR.joinpath('images').joinpath(image),
            settings.MEDIA_ROOT
        )

    for doc in documents:
        copy(
            settings.TEST_FILES_DIR.joinpath('documents').joinpath(doc),
            settings.MEDIA_ROOT
        )

def tear_down_test_files():
    rmtree(settings.MEDIA_ROOT)
