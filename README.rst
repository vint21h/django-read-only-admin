.. django-read-only-admin
.. README.rst


A django-read-only-admin documentation
======================================

|Travis|_ |Coverage|_ |Codacy|_ |Requires|_ |pypi-license|_ |pypi-version|_ |pypi-python-version|_ |pypi-django-version|_ |pypi-format|_ |pypi-wheel|_ |pypi-status|_

    *django-read-only-admin is a Django reusable application that fully implement read only admin*

.. contents::

Installation
------------
* Obtain your copy of source code from the git repository: ``git clone https://github.com/vint21h/django-read-only-admin.git``. Or download the latest release from https://github.com/vint21h/django-read-only-admin/tags/.
* Run ``python ./setup.py install`` from the repository source tree or the unpacked archive. Or use pip: ``pip install django-read-only-admin``.

Configuration
-------------
* Add ``"read_only_admin"`` to ``settings.INSTALLED_APPS``.

.. code-block:: python

    # settings.py

    INSTALLED_APPS += (
        "read_only_admin",
    )

* Run ``django-admin migrate``.
* Then add ``user/group`` ``change/delete/add/readonly`` model permissions.

django-read-only-admin settings
-------------------------------
``READONLY_ADMIN_PERMISSION_PREFIX``
    Read-only permission prefix. Defaults to: ``"readonly"``.

``READONLY_ADMIN_PERMISSION_NAME_PREFIX``
    Read-only permission name prefix. Defaults to: ``"Read only"``.

``READONLY_ADMIN_EMPTY_ACTIONS``
    Empty admin actions list (exclude superusers) or just remove delete selected action. Defaults to: ``True``.

Usage
-----
Just inherit your custom Django admin class from ``read_only_admin.admin.ReadonlyAdmin``.

.. code-block:: python

    # admin.py

    from read_only_admin.admin import ReadonlyAdmin

    class MyCustomAdmin(ReadonlyAdmin):

        pass

Also tabular and stacked inlines are supported.

.. code-block:: python

    # admin.py

    from read_only_admin.admin import (
        ReadonlyStackedInline,
        ReadonlyTabularInline,
    )

    class MyCustomTabularInline(ReadonlyTabularInline):

        model = MyModel
        extra = 0


    class MyCustomStackedInline(ReadonlyStackedInline):

        model = MyModel
        extra = 0

If you use ``list_editable`` in your custom admin classes, copy ``read_only_admin/templates/admin/pagination.html`` to your project ``templates/admin`` directory.

Licensing
---------
django-read-only-admin uses the MIT license. Please check the MIT-LICENSE file for more details.

Some part of code fairly stolen from teh internets with reference to the source. So, if you author of this code, please contact me.

Contacts
--------
**Project Website**: https://github.com/vint21h/django-read-only-admin/

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>

For other authors list see AUTHORS file.

.. |Travis| image:: https://travis-ci.org/vint21h/django-read-only-admin.svg?branch=master
.. |Coverage| image:: https://api.codacy.com/project/badge/Coverage/055abbc43fe24b5fb287bf4317530b68
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/055abbc43fe24b5fb287bf4317530b68
.. |Requires| image:: https://requires.io/github/vint21h/django-read-only-admin/requirements.svg?branch=master
.. |pypi-license| image:: https://img.shields.io/pypi/l/django-read-only-admin
.. |pypi-version| image:: https://img.shields.io/pypi/v/django-read-only-admin
.. |pypi-django-version| image:: https://img.shields.io/pypi/djversions/django-read-only-admin
.. |pypi-python-version| image:: https://img.shields.io/pypi/pyversions/django-read-only-admin
.. |pypi-format| image:: https://img.shields.io/pypi/format/django-read-only-admin
.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/django-read-only-admin
.. |pypi-status| image:: https://img.shields.io/pypi/status/django-read-only-admin
.. _Travis: https://travis-ci.org/vint21h/django-read-only-admin/
.. _Coverage: https://www.codacy.com/app/vint21h/django-read-only-admin
.. _Codacy: https://www.codacy.com/app/vint21h/django-read-only-admin
.. _Requires: https://requires.io/github/vint21h/django-read-only-admin/requirements/?branch=master
.. _pypi-license: https://pypi.org/project/django-read-only-admin/
.. _pypi-version: https://pypi.org/project/django-read-only-admin/
.. _pypi-django-version: https://pypi.org/project/django-read-only-admin/
.. _pypi-python-version: https://pypi.org/project/django-read-only-admin/
.. _pypi-format: https://pypi.org/project/django-read-only-admin/
.. _pypi-wheel: https://pypi.org/project/django-read-only-admin/
.. _pypi-status: https://pypi.org/project/django-read-only-admin/
