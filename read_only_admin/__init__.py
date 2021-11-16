# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/__init__.py


from typing import List


__all__: List[str] = ["default_app_config"]


default_app_config: str = "read_only_admin.apps.DjangoReadOnlyAdminConfig"
