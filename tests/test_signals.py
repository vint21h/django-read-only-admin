# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_signals.py


from django.contrib.auth.models import Permission
from django.test import TestCase


__all__ = ["AddReadOnlyPermissionsSignalTest"]  # type: list


class AddReadOnlyPermissionsSignalTest(TestCase):
    """
    Add read only permissions signal tests.
    """

    def test_add_readonly_permissions(self):
        """
        Test signal.
        """

        self.assertQuerysetEqual(qs=Permission.objects.all(), values=[])
