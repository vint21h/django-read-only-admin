# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_admin.py


from typing import List, Type  # pylint: disable=W0611

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.http import HttpRequest
from django.test import TestCase

from read_only_admin.admin import ReadonlyAdmin, ReadonlyChangeList


__all__ = ["ReadonlyAdminTest", "ReadonlyChangeListTest"]  # type: List[str]


User = get_user_model()


class ReadOnlyUserAdmin(UserAdmin, ReadonlyAdmin):
    """
    Read only admin class.
    """

    pass


class ReadonlyChangeListTest(TestCase):
    """
    Read only change list tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        user = User.objects.create(
            username="test",
            email="test@example.com",
            password=User.objects.make_random_password(),
            is_staff=True,
        )
        user.user_permissions.add(*list(Permission.objects.all()))
        user.save()

    def test__init__(self):
        """
        Init method must set readonly property to True.
        """

        request = HttpRequest()  # type: HttpRequest
        request.user = User.objects.first()
        result = ReadonlyChangeList(
            request=request,
            model=User,
            list_display=UserAdmin.list_display,
            list_display_links=UserAdmin.list_display_links,
            list_filter=UserAdmin.list_filter,
            date_hierarchy=UserAdmin.date_hierarchy,
            search_fields=UserAdmin.search_fields,
            list_select_related=UserAdmin.list_select_related,
            list_per_page=UserAdmin.list_per_page,
            list_max_show_all=UserAdmin.list_max_show_all,
            list_editable=UserAdmin.list_editable,
            model_admin=ReadOnlyUserAdmin(
                model=get_user_model(), admin_site=AdminSite()
            ),
            sortable_by=UserAdmin.sortable_by,
        )  # type: ReadonlyChangeList

        self.assertTrue(expr=result.readonly)


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
            password=User.objects.make_random_password(),
            is_staff=True,
        )
        user.user_permissions.add(*list(Permission.objects.all()))
        user.save()

    def test_get_changelist(self) -> None:
        """
        Method must return read only change list class.

        :return: nothing.
        :rtype: None.
        """

        request = HttpRequest()  # type: HttpRequest
        request.user = User.objects.first()
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_changelist(
            request=request
        )  # type: Type[ReadonlyChangeList]

        self.assertEqual(first=result, second=ReadonlyChangeList)
