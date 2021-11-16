# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/settings.py


import sys
import pathlib
from random import SystemRandom
from typing import Dict, List, Union


# black magic to use imports from library code
path = pathlib.Path(__file__).absolute()
project = path.parent.parent.parent
sys.path.insert(0, str(project))

# secret key
SECRET_KEY: str = "".join(
    [
        SystemRandom().choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
        for i in range(50)
    ]
)

# configure databases
DATABASES: Dict[str, Dict[str, str]] = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

# configure templates
TEMPLATES: List[Dict[str, Union[str, List[str], bool, Dict[str, str]]]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {},
    }
]


# add testing related apps
INSTALLED_APPS: List[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "read_only_admin",
]

# configure urls
ROOT_URLCONF: str = "read_only_admin.urls"

# read only admin settings
READ_ONLY_ADMIN_PERMISSION_PREFIX: str = "readonly"
READ_ONLY_ADMIN_PERMISSION_NAME_PREFIX: str = "Read only"
READ_ONLY_ADMIN_EMPTY_ACTIONS: bool = True
