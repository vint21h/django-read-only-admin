# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_admin.py


from collections import OrderedDict
from typing import Any, List, Type, Iterable  # pylint: disable=W0611

from django.contrib.admin.actions import delete_selected
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.forms.formsets import BaseFormSet  # pylint: disable=W0611
from django.http import HttpRequest
from django.test import TestCase
from django.test.utils import override_settings

from read_only_admin.admin import ReadonlyAdmin, ReadonlyChangeList


__all__ = [
    "ReadonlyAdminTest",
    "ReadonlyChangeListTest",
    "ReadonlyInlineTest",
]  # type: List[str]


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

    def test_get_changelist_formset(self) -> None:
        """
        Method must return change list form set.

        :return: nothing.
        :rtype: None.
        """

        request = HttpRequest()  # type: HttpRequest
        request.user = User.objects.first()
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_changelist_formset(
            request=request
        )  # type: BaseFormSet

        self.assertEqual(first=result.__name__, second="UserFormFormSet")

    def test_get_readonly_fields(self) -> None:
        """
        Method must return all form fields as read only.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_readonly_fields(
            request=request, obj=user
        )  # type: Iterable[str]
        expected = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "last_login",
            "date_joined",
        ]  # type: List[str]

        self.assertListEqual(list1=result, list2=expected)

    def test_get_actions(self) -> None:
        """
        Method must return empty actions list.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_actions(
            request=request
        )  # type: OrderedDict[str, Any]

        self.assertDictEqual(d1=result, d2=OrderedDict())

    @override_settings(READONLY_ADMIN_EMPTY_ACTIONS=False)
    def test_get_actions__without_empty_actions(self) -> None:
        """
        Method must return actions list resolved by available permissions.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_actions(
            request=request
        )  # type: OrderedDict[str, Any]

        self.assertDictEqual(d1=result, d2=OrderedDict())

    def test_get_readonly_fields__for_superuser(self) -> None:
        """
        Method must return empty read only fields for super user.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        user.is_superuser = True
        user.save(update_fields=["is_superuser"])
        request = HttpRequest()  # type: HttpRequest
        request.user = user
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_readonly_fields(
            request=request, obj=user
        )  # type: Iterable[str]

        self.assertEqual(first=result, second=())

    def test_get_actions__for_superuser(self) -> None:
        """
        Method must return actions list resolved by available permissions.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        user.is_superuser = True
        user.save(update_fields=["is_superuser"])
        request = HttpRequest()  # type: HttpRequest
        request.user = user
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_actions(
            request=request
        )  # type: OrderedDict[str, Any]
        expected = OrderedDict(
            [
                (
                    "delete_selected",
                    (
                        delete_selected,
                        "delete_selected",
                        "Delete selected %(verbose_name_plural)s",
                    ),
                )
            ]
        )  # type: OrderedDict[str, Any]

        self.assertDictEqual(d1=result, d2=expected)

    @override_settings(READONLY_ADMIN_EMPTY_ACTIONS=False)
    def test_get_actions__without_empty_actions__for_superuser(self) -> None:
        """
        Method must return actions list resolved by available permissions.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        user.is_superuser = True
        user.save(update_fields=["is_superuser"])
        request = HttpRequest()  # type: HttpRequest
        request.user = user
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_actions(
            request=request
        )  # type: OrderedDict[str, Any]
        expected = OrderedDict(
            [
                (
                    "delete_selected",
                    (
                        delete_selected,
                        "delete_selected",
                        "Delete selected %(verbose_name_plural)s",
                    ),
                )
            ]
        )  # type: OrderedDict[str, Any]

        self.assertDictEqual(d1=result, d2=expected)


class ReadonlyInlineTest(TestCase):
    """
    Read only inline tests.
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