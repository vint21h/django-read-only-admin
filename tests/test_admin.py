# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_admin.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test import TestCase

from read_only_admin.admin import ReadonlyAdmin, ReadonlyChangeList


__all__ = ["ReadonlyAdminTest"]  # type: List[str]


User = get_user_model()


class ReadOnlyUserAdmin(UserAdmin, ReadonlyAdmin):
    """
    Read only admin class.
    """

    pass


# unregister default admin class
admin.site.unregister(User)
# register read only admin class
admin.site.reregister(User, ReadOnlyUserAdmin)


class ReadonlyAdminTest(TestCase):
    """
    Read only admin tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        user = User.objects.create(
            username="test",
            email="test@example.com",
            password="super-secret-password",
            is_staff=True,
        )
        user.user_permissions.add(*list(Permission.objects.all()))
        user.save()

    def setUp(self):
        """
        Setup.
        """

        self.request = HttpRequest()  # type: HttpRequest
        setattr(self.request, "session", "session")
        setattr(self.request, "_messages", FallbackStorage(self.request))

    def test_get_changelist(self) -> None:
        """
        Method must return read only change list class.

        :return: nothing.
        :rtype: None.
        """

        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_changelist(request=self.request)

        self.assertEqual(first=result, second=ReadonlyChangeList)
