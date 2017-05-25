# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/admin.py

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets

from read_only_admin.settings import PERMISSION_PREFIX


__all__ = [
    "ReadonlyAdmin",
]


class ReadonlyAdmin(admin.ModelAdmin):
    """
    Readonly admin.
    """

    def get_readonly_fields(self, request, obj=None):
        """
        Get readonly fields.
        Get from: https://github.com/anupamshakya7/django-admin-hack/.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :param obj: An object.
        :type obj: django.db.models.Model.
        :return: readonly fields.
        :rtype: list.
        """

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(".")
            perm = "{prefix}_{model}".format(**{
                "prefix": PERMISSION_PREFIX,
                "model": self.model.__name__.lower(),
            })
            if str(perm) == str(tail):
                if request.user.has_perm(str(permission)) and not request.user.is_superuser:
                    if self.declared_fieldsets:

                        return flatten_fieldsets(self.declared_fieldsets)
                    else:

                        return list(set([field.name for field in self.opts.local_fields] + [field.name for field in self.opts.local_many_to_many]))

        return self.readonly_fields

    def get_actions(self, request):
        """
        Get actions (remove 'delete selected' action).
        Get from: http://vinitkumar.me/articles/2014/05/18/Get-Readonly-Mode-IN-Django/.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :return: admin actions.
        :rtype: dict.
        """

        actions = super(ReadonlyAdmin, self).get_actions(request)
        perm = "{app}.{prefix}_{model}".format(**{
            "app": self.model._meta.app_label,
            "prefix": PERMISSION_PREFIX,
            "model": self.model.__name__.lower(),
        })

        if request.user.has_perm(perm) and not request.user.is_superuser:
            if "delete_selected" in actions:
                del actions["delete_selected"]

            return actions
        else:

            return actions
