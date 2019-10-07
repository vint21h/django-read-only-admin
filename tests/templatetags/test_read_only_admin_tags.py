# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/templatetags/test_read_only_admin_tags.py


from typing import List  # pylint: disable=W0611

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.http import HttpRequest
from django.template import Context, RequestContext
from django.test import TestCase

from read_only_admin.conf import settings
from read_only_admin.templatetags.read_only_admin_tags import (
    unescape,
    readonly_submit_row,
)


__all__ = [
    "UnescapeTemplatetagTest",
    "ReadonlySubmitRowTemplatetagTest",
]  # type: List[str]


User = get_user_model()


class UnescapeTemplatetagTest(TestCase):
    """
    Unescape templatetag tests.
    """

    def test_unescape(self) -> None:
        """
        Test templatetag.

        :return: nothing.
        :rtype: None.
        """

        escaped = """&lt;script type=&quot;text/javascript&quot;&gt;alert(&#39;PWND &amp; HACKD!!1&#39;)&lt;/script&gt;"""  # noqa: E501, type: str
        unescaped = (
            """<script type="text/javascript">alert('PWND & HACKD!!1')</script>"""
        )  # noqa: E501, type: str

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__single_quote(self) -> None:
        """
        Test templatetag for single quote char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&#39;"  # type: str
        unescaped = "'"  # type: str

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__double_quote(self) -> None:
        """
        Test templatetag for double quote char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&quot;"  # type: str
        unescaped = '"'  # type: str

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__less_than(self) -> None:
        """
        Test templatetag for less than char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&lt;"  # type: str
        unescaped = "<"  # type: str

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__great_than(self) -> None:
        """
        Test templatetag for great than char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&gt;"  # type: str
        unescaped = ">"  # type: str

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__ampersand(self) -> None:
        """
        Test templatetag for ampersand char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&amp;"  # type: str
        unescaped = "&"  # type: str

        self.assertEqual(first=unescape(value=escaped), second=unescaped)


class ReadonlySubmitRowTemplatetagTest(TestCase):
    """
    Read only submit row templatetag tests.
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

    def test_readonly_submit_row__return_context(self) -> None:
        """
        Test templatetag return context.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        context = RequestContext(
            request=request,
            dict_={
                "user": user,
                "add": True,
                "change": True,
                "is_popup": False,
                "save_as": True,
                "has_add_permission": True,
                "has_change_permission": True,
                "has_view_permission": True,
                "has_editable_inline_admin_formsets": False,
                "has_delete_permission": True,
                "opts": "auth.user",
                "request": request,
            },
        )  # type: RequestContext
        result = readonly_submit_row(context=context)  # type: Context

        self.assertIsInstance(obj=result, cls=Context)

    def test_readonly_submit_row(self) -> None:
        """
        Test templatetag.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        context = RequestContext(
            request=request,
            dict_={
                "user": user,
                "add": True,
                "change": True,
                "is_popup": False,
                "save_as": True,
                "has_add_permission": True,
                "has_change_permission": True,
                "has_view_permission": True,
                "has_editable_inline_admin_formsets": False,
                "has_delete_permission": True,
                "opts": "auth.user",
                "request": request,
            },
        )  # type: RequestContext
        result = readonly_submit_row(context=context)  # type: Context

        self.assertFalse(expr=result["show_delete_link"])
        self.assertFalse(expr=result["show_save_and_add_another"])
        self.assertFalse(expr=result["show_save_and_continue"])
        self.assertFalse(expr=result["show_save"])

    def test_readonly_submit_row__for_superuser(self) -> None:
        """
        Test templatetag for superuser.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        user.is_superuser = True  # type: ignore
        user.save(update_fields=["is_superuser"])  # type: ignore
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        context = RequestContext(
            request=request,
            dict_={
                "user": user,
                "add": True,
                "change": True,
                "is_popup": False,
                "save_as": True,
                "has_add_permission": True,
                "has_change_permission": True,
                "has_view_permission": True,
                "has_editable_inline_admin_formsets": False,
                "has_delete_permission": True,
                "opts": "auth.user",
                "request": request,
            },
        )  # type: RequestContext
        result = readonly_submit_row(context=context)  # type: Context

        self.assertTrue(expr=result["show_delete_link"])
        self.assertTrue(expr=result["show_save_and_add_another"])
        self.assertTrue(expr=result["show_save_and_continue"])
        self.assertTrue(expr=result["show_save"])

    def test_readonly_submit_row__without__read_only_permissions(self) -> None:
        """
        Test templatetag without read only permissions.

        :return: nothing.
        :rtype: None.
        """

        Permission.objects.filter(
            codename__startswith=settings.READONLY_ADMIN_PERMISSION_PREFIX
        ).delete()

        user = User.objects.first()
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        context = RequestContext(
            request=request,
            dict_={
                "user": user,
                "add": True,
                "change": True,
                "is_popup": False,
                "save_as": True,
                "has_add_permission": True,
                "has_change_permission": True,
                "has_view_permission": True,
                "has_editable_inline_admin_formsets": False,
                "has_delete_permission": True,
                "opts": "auth.user",
                "request": request,
            },
        )  # type: RequestContext
        result = readonly_submit_row(context=context)  # type: Context

        self.assertTrue(expr=result["show_delete_link"])
        self.assertTrue(expr=result["show_save_and_add_another"])
        self.assertTrue(expr=result["show_save_and_continue"])
        self.assertTrue(expr=result["show_save"])

    def test_readonly_submit_row__without__read_only_permissions__for_superuser(
        self
    ) -> None:
        """
        Test templatetag without read only permissions for superuser.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        user.is_superuser = True  # type: ignore
        user.save(update_fields=["is_superuser"])  # type: ignore
        request = HttpRequest()  # type: HttpRequest
        request.user = user  # type: ignore
        context = RequestContext(
            request=request,
            dict_={
                "user": user,
                "add": True,
                "change": True,
                "is_popup": False,
                "save_as": True,
                "has_add_permission": True,
                "has_change_permission": True,
                "has_view_permission": True,
                "has_editable_inline_admin_formsets": False,
                "has_delete_permission": True,
                "opts": "auth.user",
                "request": request,
            },
        )  # type: RequestContext
        result = readonly_submit_row(context=context)  # type: Context

        self.assertTrue(expr=result["show_delete_link"])
        self.assertTrue(expr=result["show_save_and_add_another"])
        self.assertTrue(expr=result["show_save_and_continue"])
        self.assertTrue(expr=result["show_save"])
