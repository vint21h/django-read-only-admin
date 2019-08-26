# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/settings.py


import pathlib
import sys


# black magic to use imports from library code
sys.path.insert(0, str(pathlib.Path(__file__).absolute().parent.parent.parent))

# secret key
SECRET_KEY = "django-read-only-admin-test-key"  # type: str

# configure databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "django-read-only-admin-tests.sqlite3",
    }
}  # type: dict

# configure templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {},
    }
]  # type: list


# add testing related apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django_nose",
    "read_only_admin",
]  # type: list

# add nose test runner
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"  # type: str

# configure nose test runner
NOSE_ARGS = [
    "--rednose",
    "--force-color",
    "--with-timer",
    "--with-doctest",
    "--with-coverage",
    "--cover-inclusive",
    "--cover-erase",
    "--cover-package=opensearch",
    "--logging-clear-handlers",
]  # type: list

# configure urls
ROOT_URLCONF = "read_only_admin.urls"  # type: str

# read only admin settings
READONLY_ADMIN_PERMISSION_PREFIX = "readonly"  # type: str
READONLY_ADMIN_PERMISSION_NAME_PREFIX = "Read only"  # type: str
READONLY_ADMIN_EMPTY_ACTIONS = True  # type: bool
