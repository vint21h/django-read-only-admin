# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/conf.py


from typing import List  # pylint: disable=W0611

from appconf import AppConf
from django.conf import settings


__all__ = ["settings"]  # type: List[str]


class DjangoReadOnlyAdminAppConf(AppConf):
    """
    Django read only admin settings.
    """

    PERMISSION_PREFIX = getattr(
        settings, "READONLY_ADMIN_PERMISSION_PREFIX", "readonly"
    )  # type: str
    PERMISSION_NAME_PREFIX = getattr(
        settings, "READONLY_ADMIN_PERMISSION_NAME_PREFIX", "Read only"
    )  # type: str
    EMPTY_ACTIONS = getattr(
        settings, "READONLY_ADMIN_EMPTY_ACTIONS", True
    )  # type: bool

    class Meta:

        prefix = "read_only_admin"  # type: str
