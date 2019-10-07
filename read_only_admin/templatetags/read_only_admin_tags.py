# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/templatetags/read_only_admin_tags.py


from typing import Dict, List  # pylint: disable=W0611

from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row

from read_only_admin.utils import get_read_only_permission_codename


__all__ = ["unescape", "readonly_submit_row"]  # type: List[str]


register = template.Library()

_HTML_UNESCAPES = {
    "&#39;": "'",
    "&quot;": '"',
    "&gt;": ">",
    "&lt;": "<",
    "&amp;": "&",
}  # type: Dict[str, str]


@register.filter()
def unescape(value: str) -> str:
    """
    Returns the ASCII decoded version of the given HTML string. This does NOT remove normal HTML tags like <p>.  # noqa: E501
    Get from: https://stackoverflow.com/questions/275174/how-do-i-perform-html-decoding-encoding-using-python-django.  # noqa: E501

    :param value: string wanted to decoded.
    :type value: str.
    :return: decoded string.
    :rtype: str.
    """

    for code, char in _HTML_UNESCAPES.items():
        value = value.replace(code, char)

    return value


@register.inclusion_tag("admin/submit_line.html", takes_context=True)
def readonly_submit_row(context: template.RequestContext) -> template.Context:
    """
    Read only submit row templatetag.
    Get from: http://anupamshakya.blogspot.com/2013/07/create-readonly-permission-for-all.html.  # noqa: E501

    :param context: template context.
    :type context: django.template.RequestContext.
    :return: updated context.
    :rtype: django.template.Context.
    """

    ctx = submit_row(context=context)  # type: template.Context
    app, separator, model = context["opts"].partition(  # pylint: disable=W0612
        "."
    )  # type: str, str, str
    user = context["request"].user

    for permission in user.get_all_permissions():
        head, sep, tail = permission.partition(  # pylint: disable=W0612
            "."
        )  # type: str, str, str
        if get_read_only_permission_codename(model=model) == tail:
            if user.has_perm(permission) and not user.is_superuser:
                ctx.update(
                    {
                        "show_delete_link": False,
                        "show_save_and_add_another": False,
                        "show_save_and_continue": False,
                        "show_save": False,
                    }
                )

            return ctx

    return ctx
