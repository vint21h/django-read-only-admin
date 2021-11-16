# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/templatetags/read_only_admin_tags.py


from typing import Dict, List

from django.template import Context, Library, RequestContext
from django.contrib.admin.templatetags.admin_modify import submit_row

from read_only_admin.utils import get_read_only_permission_codename


__all__: List[str] = ["unescape", "readonly_submit_row"]


register = Library()

_HTML_UNESCAPES: Dict[str, str] = {
    "&#39;": "'",
    "&quot;": '"',
    "&gt;": ">",
    "&lt;": "<",
    "&amp;": "&",
}


@register.filter()
def unescape(value: str) -> str:
    """
    Returns the ASCII decoded version of the given HTML string. This does NOT remove normal HTML tags like <p>.

    Get from: https://stackoverflow.com/questions/275174/how-do-i-perform-html-decoding-encoding-using-python-django.

    :param value: string wanted to decoded
    :type value: str
    :return: decoded string
    :rtype: str
    """  # noqa: E501
    for code, char in _HTML_UNESCAPES.items():
        value = value.replace(code, char)

    return value


@register.inclusion_tag("admin/submit_line.html", takes_context=True)
def readonly_submit_row(context: RequestContext) -> Context:
    """
    Read only submit row templatetag.

    Get from: http://anupamshakya.blogspot.com/2013/07/create-readonly-permission-for-all.html.

    :param context: template context
    :type context: RequestContext
    :return: updated context
    :rtype: Context
    """  # noqa: E501
    ctx: Context = submit_row(context=context)
    app, separator, model = context["opts"].partition(  # pylint: disable=W0612
        "."
    )  # type: str, str, str
    user = context["request"].user

    for permission in user.get_all_permissions():
        head, sep, tail = permission.partition(  # pylint: disable=W0612
            "."
        )  # type: str, str, str
        if get_read_only_permission_codename(model=model) == tail and (
            user.has_perm(permission) and not user.is_superuser
        ):
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
