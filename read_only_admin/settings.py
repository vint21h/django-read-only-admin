# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/settings.py

from __future__ import unicode_literals

from django.conf import settings


__all__ = [
    "PERMISSION_PREFIX",
    "PERMISSION_NAME_PREFIX",
    "EMPTY_ACTIONS",
]


PERMISSION_PREFIX = getattr(settings, "READONLY_ADMIN_PERMISSION_PREFIX", "readonly")
PERMISSION_NAME_PREFIX = getattr(settings, "READONLY_ADMIN_PERMISSION_NAME_PREFIX", "Read only")
EMPTY_ACTIONS = getattr(settings, "READONLY_ADMIN_EMPTY_ACTIONS", True)
