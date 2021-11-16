# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/conf.py


from typing import List

from appconf import AppConf
from django.conf import settings


__all__: List[str] = ["settings"]


class DjangoReadOnlyAdminAppConf(AppConf):
    """Django read only admin settings."""

    PERMISSION_PREFIX: str = getattr(
        settings, "READ_ONLY_ADMIN_PERMISSION_PREFIX", "readonly"
    )
    PERMISSION_NAME_PREFIX: str = getattr(
        settings, "READ_ONLY_ADMIN_PERMISSION_NAME_PREFIX", "Read only"
    )
    EMPTY_ACTIONS: bool = getattr(settings, "READ_ONLY_ADMIN_EMPTY_ACTIONS", True)

    class Meta:
        """Config settings."""

        prefix: str = "read_only_admin"
