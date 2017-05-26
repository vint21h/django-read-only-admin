# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/admin.py

from __future__ import unicode_literals
from collections import OrderedDict

import django
from django.contrib import admin
from django.contrib.auth import get_permission_codename
try:
    from django.contrib.admin.utils import flatten_fieldsets
except ImportError:
    from django.contrib.admin.util import flatten_fieldsets

from read_only_admin.settings import (
    PERMISSION_PREFIX,
    EMPTY_ACTIONS,
)


__all__ = [
    "ReadonlyAdmin",
    "ReadonlyStackedInline",
    "ReadonlyTabularInline",
]


class ReadonlyAdmin(admin.ModelAdmin):
    """
    Readonly admin.
    """

    change_form_template = "read_only_admin/legacy/change_form.html" if django.VERSION < (1, 7) else "read_only_admin/modern/change_form.html"

    def get_readonly_fields(self, request, obj=None):
        """
        Get readonly fields.
        Get from: https://github.com/anupamshakya7/django-admin-hack/.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :param obj: an object.
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
                    if self.get_fieldsets(request=request, obj=obj):

                        return flatten_fieldsets(self.get_fieldsets(request=request, obj=obj))
                    else:

                        return list(set([field.name for field in self.opts.local_fields] + [field.name for field in self.opts.local_many_to_many]))

        return self.readonly_fields

    def get_actions(self, request):
        """
        Get actions.
        Get from: http://vinitkumar.me/articles/2014/05/18/Get-Readonly-Mode-IN-Django/.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :return: admin actions.
        :rtype: OrderedDict
        """

        if EMPTY_ACTIONS:
            # empty actions
            return OrderedDict()

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


class ReadonlyInline(admin.TabularInline):
    """
    Readonly admin inline.
    """

    def has_add_permission(self, request, obj=None):
        """
        Override for custom readonly permission.
        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :param obj: an object.
        :type obj: django.db.models.Model.
        :return: has user add permission.
        :rtype: bool.
        """

        if self.opts.auto_created:
            # We're checking the rights to an auto-created intermediate model,
            # which doesn't have its own individual permissions. The user needs
            # to have the change permission for the related model in order to
            # be able to do anything with the intermediate model.
            return self.has_change_permission(request, obj)

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(".")
            perm = "{prefix}_{model}".format(**{
                "prefix": PERMISSION_PREFIX,
                "model": self.model.__name__.lower(),
            })
            if str(perm) == str(tail):
                if request.user.has_perm(str(permission)) and not request.user.is_superuser:

                    return False

        codename = get_permission_codename("add", self.opts)

        return request.user.has_perm("%s.%s" % (self.opts.app_label, codename))

    def has_delete_permission(self, request, obj=None):
        """
        Override for custom readonly permission.
        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :param obj: an object.
        :type obj: django.db.models.Model.
        :return: has user delete permission.
        :rtype: bool.
        """

        if self.opts.auto_created:
            # We're checking the rights to an auto-created intermediate model,
            # which doesn't have its own individual permissions. The user needs
            # to have the change permission for the related model in order to
            # be able to do anything with the intermediate model.
            return self.has_change_permission(request, obj)

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(".")
            perm = "{prefix}_{model}".format(**{
                "prefix": PERMISSION_PREFIX,
                "model": self.model.__name__.lower(),
            })
            if str(perm) == str(tail):
                if request.user.has_perm(str(permission)) and not request.user.is_superuser:

                    return False

        codename = get_permission_codename("delete", self.opts)

        return request.user.has_perm("%s.%s" % (self.opts.app_label, codename))

    def get_readonly_fields(self, request, obj=None):
        """
        Get readonly fields.
        Get from: https://github.com/anupamshakya7/django-admin-hack/.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :param obj: an object.
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

                    return list(set([field.name for field in self.opts.local_fields] + [field.name for field in self.opts.local_many_to_many]))

        return self.readonly_fields


class ReadonlyStackedInline(ReadonlyInline):
    """
    Stacked readonly inline.
    """

    template = "admin/edit_inline/stacked.html"


class ReadonlyTabularInline(ReadonlyInline):
    """
    Tabular readonly inline.
    """

    template = "admin/edit_inline/tabular.html"
