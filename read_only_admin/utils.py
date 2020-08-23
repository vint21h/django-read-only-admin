# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/utils.py


from typing import List  # pylint: disable=W0611

from read_only_admin.conf import settings


__all__ = [
    "get_read_only_permission_codename",
    "get_read_only_permission_name",
]  # type: List[str]


def get_read_only_permission_codename(model: str) -> str:
    """
    Create read only permission code name.

    :param model: model name
    :type model: str
    :return: read only permission code name
    :rtype: str
    """

    return f"{settings.READ_ONLY_ADMIN_PERMISSION_PREFIX}_{model}"


def get_read_only_permission_name(model: str) -> str:
    """
    Create read only permission human readable name.

    :param model: model name
    :type model: str
    :return: read only permission human readable name
    :rtype: str
    """

    return f"{settings.READ_ONLY_ADMIN_PERMISSION_NAME_PREFIX.capitalize()} {model}"
