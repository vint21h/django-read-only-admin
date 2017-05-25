# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/apps.py

from __future__ import unicode_literals

from django.apps import AppConfig


__all__ = [
    "Config",
]


class Config(AppConfig):

    name = "read_only_admin"
    verbose_name = "Django read only admin"
