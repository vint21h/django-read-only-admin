# -*- coding: utf-8 -*-

# django-read-only-admin
# read_only_admin/admin.py


from functools import partial
from collections import OrderedDict
from typing import (  # pylint: disable=W0611
    Any,
    Dict,
    List,
    Type,
    Tuple,
    Union,
    Callable,
    Optional,
)

from django.db.models import Model
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_permission_codename
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin import ModelAdmin, TabularInline
from django.forms.models import BaseModelFormSet, modelformset_factory

from read_only_admin.conf import settings
from read_only_admin.utils import get_read_only_permission_codename


__all__ = [
    "ReadonlyAdmin",
    "ReadonlyStackedInline",
    "ReadonlyTabularInline",
]  # type: List[str]


class ReadonlyChangeList(ChangeList):
    """
    Readonly admin change list.
    """

    def __init__(
        self,
        request: WSGIRequest,
        model: Type[Model],
        list_display: Union[List[Union[Callable, str]], Tuple[str]],  # type: ignore
        list_display_links: Optional[  # type: ignore
            Union[List[Callable], List[str], Tuple[str]]
        ],
        list_filter: Union[List[Type[SimpleListFilter]], List[str], Tuple[str]],
        date_hierarchy: Optional[str],
        search_fields: Union[List[str], Tuple[str]],
        list_select_related: Union[Tuple[str], bool],
        list_per_page: int,
        list_max_show_all: int,
        list_editable: Union[List[str], Tuple[str]],
        model_admin: ModelAdmin,
        sortable_by: Union[List[Callable], List[str], Tuple[str]],  # type: ignore
    ) -> None:
        """
        Overridden to set extra readonly property.

        :param request: django WSGI request object
        :type request: WSGIRequest
        :param model: django related model
        :type model: Type[Model]
        :param list_display: list of fields to display
        :type list_display: Union[List[Union[Callable, str]], Tuple[str]]
        :param list_display_links: list of fields to display as links
        :type list_display_links: Optional[Union[List[Callable], List[str], Tuple[str]]]
        :param list_filter: list of fields by which can be filtering do
        :type list_filter: Union[List[Type[SimpleListFilter]], List[str], Tuple[str]]
        :param date_hierarchy: generate date hierarchy for field name
        :type date_hierarchy: Optional[str]
        :param search_fields: list of fields by which can be search do
        :type search_fields: Union[List[str], Tuple[str]]
        :param list_select_related: select related fields
        :type list_select_related: Union[Tuple[str], bool]
        :param list_per_page: items on page number
        :type list_per_page: int
        :param list_max_show_all:  how many items can appear on a show all change list page
        :type list_max_show_all: int
        :param list_editable: list of inline editable fields
        :type list_editable: Union[List[str], Tuple[str]]
        :param model_admin: django related admin
        :type model_admin: ModelAdmin
        :param sortable_by: brute enable/disable sorting for list of fields
        :type sortable_by: Union[List[Callable], List[str], Tuple[str]]
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
            head, sep, tail = permission.partition(  # pylint: disable=W0612
                "."
            )  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
                    and not request.user.is_superuser  # noqa: W503
                ):
                    self.readonly = True


class ReadonlyAdmin(ModelAdmin):
    """
    Readonly admin.
    """

    change_form_template = "read_only_admin/change_form.html"  # type: str

    def get_changelist(  # pylint: disable=R0201
        self, request: HttpRequest, **kwargs: Dict[str, Any]
    ) -> Type[ReadonlyChangeList]:
        """
        Returns the ReadonlyChangeList class for use on the changelist page.

        :param request: django HTTP request object
        :type request: HttpRequest
        :param kwargs: additional args
        :type kwargs: Dict[str, Any]
        :return: readonly change list
        :rtype: ReadonlyChangeList
        """

        return ReadonlyChangeList

    def get_changelist_formset(
        self, request: HttpRequest, **kwargs: Dict[str, Any]
    ) -> Type[BaseModelFormSet]:
        """
        Empty FormSet class for use on the changelist page if list_editable and readonly permission is used.  # noqa: E501

        :param request: django HTTP request object
        :type request: HttpRequest
        :param kwargs: additional args
        :type kwargs: Dict[str, Any]
        :return: FormSet for changelist
        :rtype: BaseModelFormSet
        """

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(  # pylint: disable=W0612
                "."
            )  # type: str, str, str
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
                    defaults.update(kwargs)  # type: ignore

                    return modelformset_factory(
                        self.model,
                        self.get_changelist_form(request),
                        extra=0,
                        fields=(),
                        **defaults  # type: ignore
                    )

        return super(ReadonlyAdmin, self).get_changelist_formset(
            request=request, **kwargs
        )

    def get_readonly_fields(
        self, request: HttpRequest, obj: Optional[Model] = None
    ) -> Union[List[str], Tuple[str]]:
        """
        Get readonly fields.
        Get from: https://github.com/anupamshakya7/django-admin-hack/.

        :param request: django HTTP request object
        :type request: HttpRequest
        :param obj: an object
        :type obj: Model
        :return: readonly fields
        :rtype: Union[List[str], Tuple[str]]
        """

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(  # pylint: disable=W0612
                "."
            )  # type: str, str, str
            if (
                get_read_only_permission_codename(model=self.model.__name__.lower())
                == tail  # noqa: W503
            ):
                if (
                    request.user.has_perm(permission)
                    and not request.user.is_superuser  # noqa: W503
                ):
                    if self.get_fieldsets(request=request, obj=obj):

                        return flatten_fieldsets(  # type: ignore
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

    def get_actions(self, request: HttpRequest) -> "OrderedDict[str, Any]":
        """
        Get actions.
        Get from: https://vinitkumar.me/articles/2014/05/18/Get-Readonly-Mode-IN-Django.html.  # noqa: E501

        :param request: django HTTP request object
        :type request: HttpRequest
        :return: admin actions
        :rtype: OrderedDict[str, Any]
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


class ReadonlyInline(TabularInline):
    """
    Readonly admin inline.
    """

    def has_add_permission(  # pylint: disable=W0221
        self, request: HttpRequest, obj: Optional[Model] = None
    ) -> bool:
        """
        Overridden for custom readonly permission.

        :param request: django HTTP request object
        :type request: HttpRequest
        :param obj: an object
        :type obj: Model
        :return: has user add permission
        :rtype: bool
        """

        if self.opts.auto_created:
            # We're checking the rights to an auto-created intermediate model,
            # which doesn't have its own individual permissions. The user needs
            # to have the change permission for the related model in order to
            # be able to do anything with the intermediate model.
            return self.has_change_permission(request, obj)

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(  # pylint: disable=W0612
                "."
            )  # type: str, str, str
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

    def has_delete_permission(self, request, obj=None) -> bool:
        """
        Overridden for custom readonly permission.

        :param request: django HTTP request object
        :type request: HttpRequest
        :param obj: an object
        :type obj: Model
        :return: has user delete permission
        :rtype: bool
        """

        if self.opts.auto_created:
            # We're checking the rights to an auto-created intermediate model,
            # which doesn't have its own individual permissions. The user needs
            # to have the change permission for the related model in order to
            # be able to do anything with the intermediate model.
            return self.has_change_permission(request, obj)

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(  # pylint: disable=W0612
                "."
            )  # type: str, str, str
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

    def get_readonly_fields(self, request, obj=None) -> List[str]:
        """
        Get readonly fields.
        Get from: https://github.com/anupamshakya7/django-admin-hack/.

        :param request: django HTTP request object
        :type request: HttpRequest
        :param obj: an object
        :type obj: Model
        :return: readonly fields
        :rtype: list
        """

        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition(  # pylint: disable=W0612
                "."
            )  # type: str, str, str
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

    template = "admin/edit_inline/stacked.html"  # type: str


class ReadonlyTabularInline(ReadonlyInline):
    """
    Tabular readonly inline.
    """

    template = "admin/edit_inline/tabular.html"  # type: str
