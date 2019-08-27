# -*- coding: utf-8 -*-

# django-read-only-admin
# tests/templatetags/test_read_only_admin_tags.py


from django.test import TestCase

from read_only_admin.templatetags.read_only_admin_tags import unescape


__all__ = ["UnescapeTemplatetagTest"]  # type: list


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
