# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/models.py


from typing import List  # pylint: disable=W0611

from django.db.models import signals

from read_only_admin.signals import add_readonly_permissions


__all__ = []  # type: List[str]


signals.post_migrate.connect(add_readonly_permissions)
