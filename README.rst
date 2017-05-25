.. django-read-only-admin
.. README.rst

A django-read-only-admin documentation
======================================

    *django-read-only-admin is a django reusable application that fully implement read only admin*

.. contents::

Installation
------------
* Obtain your copy of source code from the git repository: ``git clone https://github.com/vint21h/django-read-only-admin.git``. Or download the latest release from https://github.com/vint21h/django-read-only-admin/tags/.
* Run ``python ./setup.py install`` from the repository source tree or the unpacked archive. Or use pip: ``pip install django-read-only-admin``.

Configuration
-------------
Add ``"read_only_admin"`` to ``settings.INSTALLED_APPS``.

.. code-block:: python

    INSTALLED_APPS += (
        "read_only_admin",
    )

Usage
-----
Just inherit your custom django admin class from ``read_only_admin.admin.ReadonlyAdmin``.

For example:

.. code-block:: python

    from read_only_admin.admin import ReadonlyAdmin

    class MyCustomAdmin(ReadonlyAdmin):
        pass


Settings
--------
``READONLY_ADMIN_PERMISSION_PREFIX``
    Read only permission prefix. Defaults to: ``readonly``.

``READONLY_ADMIN_PERMISSION_NAME_PREFIX``
    Read only permission name prefix. Defaults to: ``Read only``.

``READONLY_ADMIN_EMPTY_ACTIONS``
    Empty admin actions list or just remove delete selected action. Defaults to: ``True``.


Licensing
---------
django-read-only-admin uses the MIT license. Please check the MIT-LICENSE file for more details.

Contacts
--------
**Project Website**: https://github.com/vint21h/django-read-only-admin/

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>

For other authors list see AUTHORS file.
