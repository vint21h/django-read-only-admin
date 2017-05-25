# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/models.py

from __future__ import unicode_literals

import django
from django.db.models import signals

from read_only_admin.signals import add_readonly_permissions


__all__ = []


# connect signal
if django.VERSION < (1, 7):
    signals.post_syncdb.connect(add_readonly_permissions)
else:
    signals.post_migrate.connect(add_readonly_permissions)
