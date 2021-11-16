# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/apps.py


from typing import List

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


__all__: List[str] = ["DjangoReadOnlyAdminConfig"]


class DjangoReadOnlyAdminConfig(AppConfig):
    """Application config."""

    name: str = "read_only_admin"
    verbose_name: str = _("Django read only admin")
