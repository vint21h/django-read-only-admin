# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/apps.py


from django.apps import AppConfig
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from read_only_admin.signals import add_readonly_permissions


__all__ = ["DjangoReadOnlyAdminConfig"]  # type: list


class DjangoReadOnlyAdminConfig(AppConfig):
    """
    Application config.
    """

    name = "read_only_admin"  # type: str
    verbose_name = _("Django read only admin")  # type: str

    def ready(self) -> None:
        """
        Application read callback.

        :return: nothing.
        :rtype: None.
        """

        signals.post_migrate.connect(add_readonly_permissions)
