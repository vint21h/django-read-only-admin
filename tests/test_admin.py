# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/test_admin.py


from io import StringIO
from collections import OrderedDict
from typing import Any, List, Type, Iterable  # pylint: disable=W0611

from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.test.utils import override_settings
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.admin.actions import delete_selected
from django.forms.formsets import BaseFormSet  # pylint: disable=W0611

from read_only_admin.admin import ReadonlyAdmin, ReadonlyChangeList


__all__ = ["ReadonlyAdminTest", "ReadonlyChangeListTest"]  # type: List[str]


User = get_user_model()


class ReadOnlyUserAdmin(UserAdmin, ReadonlyAdmin):
    """
    Read only admin class.
    """

    pass  # pylint: disable=W0107


class ReadonlyChangeListTest(TestCase):
    """
    Read only change list tests.
    """

    @classmethod
    def setUpTestData(cls) -> None:
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

    def test__init__(self) -> None:
        """
        Init method must set readonly property to True.
        """

        request = WSGIRequest(
            {"REQUEST_METHOD": "GET", "PATH_INFO": "/", "wsgi.input": StringIO()}
        )  # type: WSGIRequest
        request.user = User.objects.first()  # type: ignore
        result = ReadonlyChangeList(
            request=request,
            model=User,
            list_display=[],
            list_display_links=None,
            list_filter=["is_active"],
            date_hierarchy=UserAdmin.date_hierarchy,
            search_fields=[],
            list_select_related=False,
            list_per_page=UserAdmin.list_per_page,
            list_max_show_all=UserAdmin.list_max_show_all,
            list_editable=[],
            model_admin=ReadOnlyUserAdmin(
                model=get_user_model(), admin_site=AdminSite()
            ),
            sortable_by=UserAdmin.sortable_by,  # type: ignore
        )  # type: ReadonlyChangeList

        self.assertTrue(expr=result.readonly)


class ReadonlyAdminTest(TestCase):
    """
    Read only admin tests.
    """

    @classmethod
    def setUpTestData(cls) -> None:
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
        """

        request = HttpRequest()  # type: HttpRequest
        request.user = User.objects.first()  # type: ignore
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_changelist(
            request=request
        )  # type: Type[ReadonlyChangeList]

        self.assertEqual(first=result, second=ReadonlyChangeList)

    def test_get_changelist_formset(self) -> None:
        """
        Method must return change list form set.
        """

        request = HttpRequest()  # type: HttpRequest
        request.user = User.objects.first()  # type: ignore
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_changelist_formset(
            request=request
        )  # type: Type[BaseFormSet]

        self.assertEqual(first=result.__name__, second="UserFormFormSet")

    def test_get_readonly_fields(self) -> None:
        """
        Method must return all form fields as read only.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_readonly_fields(request=request, obj=user)
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

        self.assertListEqual(list1=result, list2=expected)  # type: ignore

    def test_get_actions(self) -> None:
        """
        Method must return empty actions list.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_actions(
            request=request
        )  # type: OrderedDict[str, Any]

        self.assertDictEqual(d1=result, d2=OrderedDict())

    @override_settings(READ_ONLY_ADMIN_EMPTY_ACTIONS=False)
    def test_get_actions__without_empty_actions(self) -> None:
        """
        Method must return actions list resolved by available permissions.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_actions(
            request=request
        )  # type: OrderedDict[str, Any]

        self.assertDictEqual(d1=result, d2=OrderedDict())

    def test_get_readonly_fields__for_superuser(self) -> None:
        """
        Method must return empty read only fields for super user.
        """

        user = User.objects.first()
        user.is_superuser = True  # type: ignore
        user.save(update_fields=["is_superuser"])  # type: ignore
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        result = ReadOnlyUserAdmin(
            model=get_user_model(), admin_site=AdminSite()
        ).get_readonly_fields(
            request=request, obj=user
        )  # type: Iterable[str]

        self.assertEqual(first=result, second=())

    def test_get_actions__for_superuser(self) -> None:
        """
        Method must return actions list resolved by available permissions.
        """

        user = User.objects.first()
        user.is_superuser = True  # type: ignore
        user.save(update_fields=["is_superuser"])  # type: ignore
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
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

    @override_settings(READ_ONLY_ADMIN_EMPTY_ACTIONS=False)
    def test_get_actions__without_empty_actions__for_superuser(self) -> None:
        """
        Method must return actions list resolved by available permissions.
        """

        user = User.objects.first()
        user.is_superuser = True  # type: ignore
        user.save(update_fields=["is_superuser"])  # type: ignore
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
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
