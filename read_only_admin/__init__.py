# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/__init__.py


from typing import List  # pylint: disable=W0611


__all__ = ["default_app_config"]  # type: List[str]


default_app_config = "read_only_admin.apps.DjangoReadOnlyAdminConfig"  # type: str
