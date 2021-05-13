# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/settings.py


import sys
import random
import pathlib
from typing import Dict, List, Union  # pylint: disable=W0611


# black magic to use imports from library code
sys.path.insert(0, str(pathlib.Path(__file__).absolute().parent.parent.parent))

# secret key
SECRET_KEY = "".join(
    [
        random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")  # nosec
        for i in range(50)
    ]
)  # type: str

# configure databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}  # type: Dict[str, Dict[str, str]]

# configure templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {},
    }
]  # type: List[Dict[str, Union[str, List[str], bool, Dict[str, str]]]]


# add testing related apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "read_only_admin",
]  # type: List[str]

# configure urls
ROOT_URLCONF = "read_only_admin.urls"  # type: str

# read only admin settings
READ_ONLY_ADMIN_PERMISSION_PREFIX = "readonly"  # type: str
READ_ONLY_ADMIN_PERMISSION_NAME_PREFIX = "Read only"  # type: str
READ_ONLY_ADMIN_EMPTY_ACTIONS = True  # type: bool
