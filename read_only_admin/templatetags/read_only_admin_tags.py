# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/templatetags/read_only_admin_tags.py

from __future__ import unicode_literals

from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row

from read_only_admin.settings import PERMISSION_PREFIX


__all__ = [
    "unescape",
    "readonly_submit_row",
]


register = template.Library()


@register.filter()
def unescape(value):
    """
    Returns the ASCII decoded version of the given HTML string. This does NOT remove normal HTML tags like <p>.
    Get from: https://stackoverflow.com/questions/275174/how-do-i-perform-html-decoding-encoding-using-python-django.
    :param value: string wanted to decoded.
    :type value: unicode.
    :return: decoded string.
    :rtype: unicode.
    """

    codes = (("'", "&#39;"), ('"', "&quot;"), (">", "&gt;"), ("<", "&lt;"), ("&", "&amp;"))

    for code in codes:
        value = value.replace(code[1], code[0])

    return value


@register.inclusion_tag("admin/submit_line.html", takes_context=True)
def readonly_submit_row(context):
    """
    Read only submit row templatetag.
    Get from: http://anupamshakya.blogspot.com/2013/07/create-readonly-permission-for-all.html.

    :param context: template context.
    :type context: django.template.RequestContext.
    :return: updated context.
    :rtype: django.template.RequestContext.
    """

    ctx = submit_row(context)
    app, separator, model = str(context["opts"]).partition(".")
    user = context["request"].user

    for permission in user.get_all_permissions():
        head, sep, tail = permission.partition(".")
        perm = "{prefix}_{model}".format(**{
            "prefix": PERMISSION_PREFIX,
            "model": model,
        })
        if str(perm) == str(tail):
            if user.has_perm(str(permission)) and not user.is_superuser:
                ctx.update({
                    "show_delete_link": False,
                    "show_save_and_add_another": False,
                    "show_save_and_continue": False,
                    "show_save": False,
                })

            return ctx

    return ctx
