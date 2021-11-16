# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_signals.py


from typing import List

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import Permission


__all__: List[str] = ["AddReadOnlyPermissionsSignalTest"]


class AddReadOnlyPermissionsSignalTest(TestCase):
    """Add read only permissions signal tests."""

    def test_add_readonly_permissions(self) -> None:
        """Test signal."""
        self.assertListEqual(
            list1=list(
                Permission.objects.filter(
                    codename__startswith=settings.READ_ONLY_ADMIN_PERMISSION_PREFIX
                ).values_list("codename", flat=True)
            ),
            list2=[
                "readonly_logentry",
                "readonly_group",
                "readonly_permission",
                "readonly_user",
                "readonly_contenttype",
            ],
        )

    def test_add_readonly_permissions__count(self) -> None:
        """Test signal create new permissions number."""
        self.assertEqual(
            first=Permission.objects.filter(
                codename__startswith=settings.READ_ONLY_ADMIN_PERMISSION_PREFIX
            ).count(),
            second=5,
        )
