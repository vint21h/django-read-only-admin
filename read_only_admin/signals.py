# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/signals.py


from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from read_only_admin.conf import settings


__all__ = ["add_readonly_permissions"]  # type: list


def add_readonly_permissions(sender, *args, **kwargs) -> None:
    """
    This migrate hooks takes care of adding a read only permission to all of your content types.
    Get from: https://github.com/anupamshakya7/django-admin-hack/.
    """

    for content_type in ContentType.objects.all():
        codename = f"{settings.READ_ONLY_ADMIN_PERMISSION_PREFIX}_{content_type.model}"
        name = f"{settings.READ_ONLY_ADMIN_PERMISSION_NAME_PREFIX} {content_type.model}"

        Permission.objects.get_or_create(
            content_type=content_type, codename=codename, name=name
        )
