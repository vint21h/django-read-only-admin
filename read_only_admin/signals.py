# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/signals.py

from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from read_only_admin.settings import (
    PERMISSION_PREFIX,
    PERMISSION_NAME_PREFIX,
)


__all__ = [
    "add_readonly_permissions",
]


def add_readonly_permissions(sender, *args, **kwargs):
    """
    This syncdb/migrate hooks takes care of adding a read only permission to all of your content types.
    Get from: https://github.com/anupamshakya7/django-admin-hack/.
    """

    for content_type in ContentType.objects.all():
        codename = "{prefix}_{model}".format(**{
            "prefix": PERMISSION_PREFIX,
            "model": content_type.model,
        })
        name = "{prefix} {model}".format(**{
            "prefix": PERMISSION_NAME_PREFIX,
            "model": content_type.model,
        })

        Permission.objects.get_or_create(content_type=content_type, codename=codename, name=name)
