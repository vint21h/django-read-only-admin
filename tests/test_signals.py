# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_signals.py


from typing import List  # pylint: disable=W0611

from django.conf import settings
from django.contrib.auth.models import Permission
from django.test import TestCase


__all__ = ["AddReadOnlyPermissionsSignalTest"]  # type: List[str]


class AddReadOnlyPermissionsSignalTest(TestCase):
    """
    Add read only permissions signal tests.
    """

    def test_add_readonly_permissions(self):
        """
        Test signal.
        """

        self.assertListEqual(
            list1=list(
                Permission.objects.filter(
                    codename__startswith=settings.READONLY_ADMIN_PERMISSION_PREFIX
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

    def test_add_readonly_permissions__count(self):
        """
        Test signal create new permissions number.
        """

        self.assertEqual(
            first=Permission.objects.filter(
                codename__startswith=settings.READONLY_ADMIN_PERMISSION_PREFIX
            ).count(),
            second=5,
        )
