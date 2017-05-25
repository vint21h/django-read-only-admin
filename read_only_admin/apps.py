# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/apps.py

from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from read_only_admin.signals import add_readonly_permissions


__all__ = [
    "Config",
]


class Config(AppConfig):

    name = "read_only_admin"
    verbose_name = "Django read only admin"

    def ready(self):
        """
        Implemented to connect signals.
        """

        # connect signals for modern django versions (>= 1.7)
        post_migrate.connect(add_readonly_permissions)
