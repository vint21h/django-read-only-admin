# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/admin.py


from collections import OrderedDict
from functools import partial
from typing import Union, Iterable

from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_permission_codename
from django.db import models
from django.forms.models import modelformset_factory
from django.http import HttpRequest

from read_only_admin.conf import settings
from read_only_admin.utils import get_read_only_permission_codename


__all__ = [
    "ReadonlyAdmin",
    "ReadonlyStackedInline",
    "ReadonlyTabularInline",
]  # type: list


class ReadonlyChangeList(ChangeList):
    """
    Readonly admin change list.
    """

    def __init__(
        self,
        request: HttpRequest,
        model: models.Model,
        list_display: Iterable,
        list_display_links: Iterable,
        list_filter: Iterable,
        date_hierarchy: str,
        search_fields: Iterable,
        list_select_related: Union[bool, Iterable],
        list_per_page: int,
        list_max_show_all: int,
        list_editable: Iterable,
        model_admin: admin.ModelAdmin,
        sortable_by: Iterable,
    ) -> None:
        """
        Overridden to set extra readonly property.

        :param request: django HTTP request object.
        :type request: django.http.HttpRequest.
        :param model: django related model instance.
        :type model: django.db.models.Model.
        :param list_display: list of fields to dis[lay.
        :type list_display: Iterable.
        :param list_display_links: list of fields to display as links.
        :type list_display_links: Iterable.
        :param list_filter: list of fields by which can be filtering do.
        :type list_filter: Iterable.
        :param date_hierarchy: generate date hierarchy for field name.
        :type date_hierarchy: str.
        :param search_fields: list of fields by which can be search do.
        :type search_fields: Iterable.
        :param list_select_related:
        :type list_select_related: Union[bool, Iterable].
        :param list_per_page: items on page number.
        :type list_per_page: int.
        :param list_max_show_all:  how many items can appear on a show all change list page.
        :type list_max_show_all: int.
        :param list_editable: list of inline editable fields.
        :type list_editable: Iterable.
        :param model_admin: django related admin instance.
        :type model_admin: django.contrib.admin.ModelAdmin.
        :param sortable_by: brute enable/disable sorting for list of fields.
        :type sortable_by: Iterable.
        """  # noqa: E501

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
            head, sep, tail = permission.partition(".")  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
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
        Empty FormSet class for use on the changelist page if list_editable and readonly permission is used.  # noqa: E501

        :param request: django HTTP request object.
        :type request: django.http.request.HttpRequest.
        :return: FormSet for changelist.
        :rtype: django.forms.formsets.BaseFormSet.
        """

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(".")  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
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
            head, sep, tail = permission.partition(".")  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
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
        Get from: https://vinitkumar.me/articles/2014/05/18/Get-Readonly-Mode-IN-Django.html.  # noqa: E501

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
            head, sep, tail = permission.partition(".")  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
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
            head, sep, tail = permission.partition(".")  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
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
            head, sep, tail = permission.partition(".")  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
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
