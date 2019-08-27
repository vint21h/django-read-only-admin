# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/templatetags/test_read_only_admin_tags.py


from django.contrib.auth import get_user_model
from django.template import Context
from django.test import TestCase

from read_only_admin.templatetags.read_only_admin_tags import (
    unescape,
    readonly_submit_row,
)


__all__ = ["UnescapeTemplatetagTest"]  # type: list


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

        escaped = """&lt;script type=&quot;text/javascript&quot;&gt;console.log(&#39;PWND &amp; HACKD!!1&#39;)&lt;/script&gt;"""  # noqa: E501
        unescaped = (
            """<script type="text/javascript">console.log('PWND & HACKD!!1')</script>"""
        )

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__single_quote(self) -> None:
        """
        Test templatetag for single quote char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&#39;"
        unescaped = "'"

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__double_quote(self) -> None:
        """
        Test templatetag for double quote char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&quot;"
        unescaped = '"'

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__less_than(self) -> None:
        """
        Test templatetag for less than char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&lt;"
        unescaped = "<"

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__great_than(self) -> None:
        """
        Test templatetag for great than char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&gt;"
        unescaped = ">"

        self.assertEqual(first=unescape(value=escaped), second=unescaped)

    def test_unescape__ampersand(self) -> None:
        """
        Test templatetag for ampersand char.

        :return: nothing.
        :rtype: None.
        """

        escaped = "&amp;"
        unescaped = "&"

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

        User.objects.create(
            username="test", email="test@example.com", password="super-secret-password"
        )

    def test_readonly_submit_row(self) -> None:
        """
        Test templatetag without.

        :return: nothing.
        :rtype: None.
        """

        context = Context()
        context.update({"user": User.objects.first()})

        # TODO: implement it!!1

    def test_readonly_submit_row__without__read_only_permissions(self) -> None:
        """
        Test templatetag without read only permissions.

        :return: nothing.
        :rtype: None.
        """

        context = Context()
        context.update({"user": User.objects.first()})

        # TODO: implement it!!1

    def test_readonly_submit_row__without__read_only_permissions__for_superuser(
        self
    ) -> None:
        """
        Test templatetag without read only permissions for superuser.

        :return: nothing.
        :rtype: None.
        """

        user = User.objects.first()
        user.is_stuff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])

        context = Context()
        context.update({"user": user})

        # TODO: implement it!!1
