# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/apps.py


from typing import List  # pylint: disable=W0611

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


__all__ = ["DjangoReadOnlyAdminConfig"]  # type: List[str]


class DjangoReadOnlyAdminConfig(AppConfig):
    """
    Application config.
    """

    name = "read_only_admin"  # type: str
    verbose_name = _("Django read only admin")  # type: str
