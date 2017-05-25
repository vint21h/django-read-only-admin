# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/models.py

from __future__ import unicode_literals

from django.db.models.signals import post_syncdb

from read_only_admin.signals import add_readonly_permissions


__all__ = []


# connect signals for old django versions (< 1.7)
post_syncdb.connect(add_readonly_permissions)
