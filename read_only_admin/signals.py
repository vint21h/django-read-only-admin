# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/signals.py


from typing import List, Iterable, Optional  # pylint: disable=W0611

from django.apps import AppConfig
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.utils import DEFAULT_DB_ALIAS

from read_only_admin.utils import (
    get_read_only_permission_name,
    get_read_only_permission_codename,
)


__all__ = ["add_readonly_permissions"]  # type: List[str]


def add_readonly_permissions(
    sender: AppConfig,
    app_config: AppConfig,
    verbosity: int = 1,
    interactive: bool = False,
    using: str = DEFAULT_DB_ALIAS,
    plan: Optional[Iterable[str]] = None,
    apps: Optional[Iterable[str]] = None,
    *args,
    **kwargs,
) -> None:
    """
    This migrate hooks takes care of adding a read only permission to all of your content types.  # noqa: E501
    Get from: https://github.com/anupamshakya7/django-admin-hack/.

    :param sender: installed application config instance,
    :type sender: django.apps.AppConfig.
    :param app_config: same as sender.
    :type app_config: django.apps.AppConfig.
    :param verbosity: verbosity level.
    :type verbosity: int.
    :param interactive: prompt user to input things.
    :type interactive: bool.
    :param using: db name.
    :type using: str.
    :param plan: migration plan.
    :type plan: Optional[Iterable[str]].
    :param apps:
    :type apps: Optional[Iterable[str]].
    :param args: additional arguments.
    :type args: list.
    :param kwargs: additional arguments.
    :type kwargs: dict.
    :return: nothing.
    :rtype: None.
    """

    for content_type in ContentType.objects.all():
        Permission.objects.get_or_create(
            content_type=content_type,
            codename=get_read_only_permission_codename(model=content_type.model),
            name=get_read_only_permission_name(model=content_type.model),
        )
