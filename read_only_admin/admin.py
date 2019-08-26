# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/admin.py

from __future__ import unicode_literals

from collections import OrderedDict
from functools import partial

from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_permission_codename
from django.forms.models import modelformset_factory

from read_only_admin.conf import settings


__all__ = [
    "ReadonlyAdmin",
    "ReadonlyStackedInline",
    "ReadonlyTabularInline",
]  # type: list


class ReadonlyChangeList(ChangeList):
    """
    Readonly change list.
    """

    def __init__(
        self,
        request,
        model,
        list_display,
        list_display_links,
        list_filter,
        date_hierarchy,
        search_fields,
        list_select_related,
        list_per_page,
        list_max_show_all,
        list_editable,
        model_admin,
        sortable_by,
    ):
        """
        Override to set extra readonly property.
        """

        super(ReadonlyChangeList, self).__init__(
            request=request,
            model=model,
            list_display=list_display,
            list_display_links=list_display_links,
            list_filter=list_filter,
            date_hierarchy=date_hierarchy,
            search_fields=search_fields,
            list_select_related=list_select_related,
            list_per_page=list_per_page,
            list_max_show_all=list_max_show_all,
            list_editable=list_editable,
            model_admin=model_admin,
            sortable_by=sortable_by,
        )

        self.readonly = False

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(".")
            perm = "{prefix}_{model}".format(
                **{
                    "prefix": settings.READ_ONLY_ADMIN_PERMISSION_PREFIX,
                    "model": self.model.__name__.lower(),
                }
            )
            if str(perm) == str(tail):
                if (
                    request.user.has_perm(str(permission))
                    and not request.user.is_superuser  # noqa: W503
                ):
                    self.readonly = True


class ReadonlyAdmin(admin.ModelAdmin):
    """
    Readonly admin.
    """

    change_form_template = "read_only_admin/change_form.html"

    def get_changelist(self, request, **kwargs):
        """
        Returns the ReadonlyChangeList class for use on the changelist page.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :return: readonly change list.
        :rtype: read_only_admin.admin.ReadonlyChangeList.
        """

        return ReadonlyChangeList

    def get_changelist_formset(self, request, **kwargs):
        """
        Empty FormSet class for use on the changelist page if list_editable and readonly permission is used.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :return: FormSet for changelist.
        :rtype: django.forms.formsets.BaseFormSet.
        """

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(".")
            perm = "{prefix}_{model}".format(
                **{
                    "prefix": settings.READ_ONLY_ADMIN_PERMISSION_PREFIX,
                    "model": self.model.__name__.lower(),
                }
            )
            if str(perm) == str(tail):
                if (
                    request.user.has_perm(str(permission))
                    and not request.user.is_superuser  # noqa: W503
                ):
                    defaults = {
                        "formfield_callback": partial(
                            self.formfield_for_dbfield, request=request
                        )
                    }
                    defaults.update(kwargs)

                    return modelformset_factory(
                        self.model,
                        self.get_changelist_form(request),
                        extra=0,
                        fields=(),
                        **defaults
                    )

        return super(ReadonlyAdmin, self).get_changelist_formset(
            request=request, **kwargs
        )

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
            perm = "{prefix}_{model}".format(
                **{
                    "prefix": settings.READ_ONLY_ADMIN_PERMISSION_PREFIX,
                    "model": self.model.__name__.lower(),
                }
            )
            if str(perm) == str(tail):
                if (
                    request.user.has_perm(str(permission))
                    and not request.user.is_superuser  # noqa: W503
                ):
                    if self.get_fieldsets(request=request, obj=obj):

                        return flatten_fieldsets(
                            self.get_fieldsets(request=request, obj=obj)
                        )
                    else:

                        return list(
                            set(
                                [field.name for field in self.opts.local_fields]
                                + [  # noqa: W503
                                    field.name for field in self.opts.local_many_to_many
                                ]
                            )
                        )

        return self.readonly_fields

    def get_actions(self, request):
        """
        Get actions.
        Get from: https://vinitkumar.me/articles/2014/05/18/Get-Readonly-Mode-IN-Django.html.

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :return: admin actions.
        :rtype: OrderedDict
        """

        actions = super(ReadonlyAdmin, self).get_actions(request)
        perm = "{app}.{prefix}_{model}".format(
            **{
                "app": self.model._meta.app_label,
                "prefix": settings.READ_ONLY_ADMIN_PERMISSION_PREFIX,
                "model": self.model.__name__.lower(),
            }
        )
        if request.user.has_perm(perm) and not request.user.is_superuser:
            if "delete_selected" in actions:
                del actions["delete_selected"]

        if settings.READ_ONLY_ADMIN_EMPTY_ACTIONS and not request.user.is_superuser:
            # empty actions list (exclude superusers)
            actions = OrderedDict()

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
            perm = "{prefix}_{model}".format(
                **{
                    "prefix": settings.READ_ONLY_ADMIN_PERMISSION_PREFIX,
                    "model": self.model.__name__.lower(),
                }
            )
            if str(perm) == str(tail):
                if (
                    request.user.has_perm(str(permission))
                    and not request.user.is_superuser  # noqa: W503
                ):

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
            perm = "{prefix}_{model}".format(
                **{
                    "prefix": settings.READ_ONLY_ADMIN_PERMISSION_PREFIX,
                    "model": self.model.__name__.lower(),
                }
            )
            if str(perm) == str(tail):
                if (
                    request.user.has_perm(str(permission))
                    and not request.user.is_superuser  # noqa: W503
                ):

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
            perm = "{prefix}_{model}".format(
                **{
                    "prefix": settings.READ_ONLY_ADMIN_PERMISSION_PREFIX,
                    "model": self.model.__name__.lower(),
                }
            )
            if str(perm) == str(tail):
                if (
                    request.user.has_perm(str(permission))
                    and not request.user.is_superuser  # noqa: W503
                ):

                    return list(
                        set(
                            [field.name for field in self.opts.local_fields]
                            + [  # noqa: W503
                                field.name for field in self.opts.local_many_to_many
                            ]
                        )
                    )

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
