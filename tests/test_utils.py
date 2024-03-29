# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_utils.py


from typing import List

from django.test import TestCase
from django.test.utils import override_settings

from read_only_admin.utils import (
    get_read_only_permission_name,
    get_read_only_permission_codename,
)


__all__: List[str] = [
    "GetReadOnlyPermissionCodenameUtilTest",
    "GetReadOnlyPermissionNameUtilTest",
]


class GetReadOnlyPermissionCodenameUtilTest(TestCase):
    """get_read_only_permission_codename util tests."""

    def test_get_read_only_permission_codename(self) -> None:
        """Util must return model read only permission codename based on read only prefix setting."""  # noqa: E501
        self.assertEqual(
            get_read_only_permission_codename(model="user"), "readonly_user"
        )

    @override_settings(READ_ONLY_ADMIN_PERMISSION_PREFIX="")
    def test_get_read_only_permission_codename__without_prefix(self) -> None:
        """Util must return model read only permission codename based on read only prefix setting with broken prefix settings."""  # noqa: E501
        self.assertEqual(get_read_only_permission_codename(model="user"), "_user")


class GetReadOnlyPermissionNameUtilTest(TestCase):
    """get_read_only_permission_name util tests."""

    def test_get_read_only_permission_name(self) -> None:
        """Util must return model read only permission name based on read only name prefix setting."""  # noqa: E501
        self.assertEqual(get_read_only_permission_name(model="user"), "Read only user")

    @override_settings(READ_ONLY_ADMIN_PERMISSION_NAME_PREFIX="")
    def test_get_read_only_permission_name__without_prefix(self) -> None:
        """Util must return model read only permission name based on read only name prefix setting with broken name prefix settings."""  # noqa: E501
        self.assertEqual(get_read_only_permission_name(model="user"), " user")
