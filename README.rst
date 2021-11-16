.. django-read-only-admin
.. README.rst


A django-read-only-admin documentation
======================================

|GitHub|_ |Coveralls|_ |pypi-license|_ |pypi-version|_ |pypi-python-version|_ |pypi-django-version|_ |pypi-format|_ |pypi-wheel|_ |pypi-status|_

    *django-read-only-admin is a Django reusable application that fully implement read only admin*

.. contents::

Installation
------------
* Obtain your copy of source code from the git repository: ``$ git clone https://github.com/vint21h/django-read-only-admin.git``. Or download the latest release from https://github.com/vint21h/django-read-only-admin/tags/.
* Run ``$ python ./setup.py install`` from the repository source tree or the unpacked archive. Or use pip: ``$ pip install django-read-only-admin``.

Configuration
-------------
* Add ``"read_only_admin"`` to ``settings.INSTALLED_APPS``.

.. code-block:: python

    # settings.py

    INSTALLED_APPS += [
        "read_only_admin",
    ]

* Run ``$ python ./manage.py migrate``.
* Then add ``user/group`` ``change/delete/add/readonly`` model permissions.

Settings
--------
``READ_ONLY_ADMIN_PERMISSION_PREFIX``
    Read-only permission prefix. Defaults to: ``"readonly"``.

``READ_ONLY_ADMIN_PERMISSION_NAME_PREFIX``
    Read-only permission name prefix. Defaults to: ``"Read only"``.

``READ_ONLY_ADMIN_EMPTY_ACTIONS``
    Empty admin actions list (exclude superusers) or just remove delete selected action. Defaults to: ``True``.

Usage
-----
Just inherit your custom Django admin class from ``read_only_admin.admin.ReadonlyAdmin``.

.. code-block:: python

    # admin.py

    from read_only_admin.admin import ReadonlyAdmin


    class MyCustomAdmin(ReadonlyAdmin):

        ...

Also tabular and stacked inlines are supported.

.. code-block:: python

    # admin.py

    from read_only_admin.admin import (
        ReadonlyStackedInline,
        ReadonlyTabularInline,
    )


    class MyCustomTabularInline(ReadonlyTabularInline):

        model: Type[Model] = MyModel
        extra: int = 0


    class MyCustomStackedInline(ReadonlyStackedInline):

        model: Type[Model] = MyModel
        extra: int = 0

If you use ``list_editable`` in your custom admin classes, copy ``read_only_admin/templates/admin/pagination.html`` to your project ``templates/admin`` directory.

Contributing
------------
1. `Fork it <https://github.com/vint21h/django-read-only-admin/>`_
2. Install `GNU Make <https://www.gnu.org/software/make/>`_
3. Install and configure `pyenv <https://github.com/pyenv/pyenv/>`_ and `pyenv-virtualenv plugin <https://github.com/pyenv/pyenv-virtualenv/>`_
4. Install and configure `direnv <https://github.com/direnv/direnv/>`_
5. Create environment config from example

.. code-block:: bash

    cp .env.example .env

6. Install development dependencies:

.. code-block:: bash

    make install

7. Create your fix/feature branch:

.. code-block:: bash

    git checkout -b my-new-fix-or-feature

8. Check code style and moreover:

.. code-block:: bash

    make check

9. Run tests:

.. code-block:: bash

    make test

10. Push to the branch:

.. code-block:: bash

    git push origin my-new-fix-or-feature

11. `Create a new Pull Request <https://github.com/vint21h/django-read-only-admin/compare/>`_

Licensing
---------
django-read-only-admin uses the MIT license. Please check the MIT-LICENSE file for more details.

Some part of code fairly stolen from teh internets with reference to the source. So, if you author of this code, please contact me.

Contacts
--------
**Project Website**: https://github.com/vint21h/django-read-only-admin/

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>

For other authors list see AUTHORS file.

.. |GitHub| image:: https://github.com/vint21h/django-read-only-admin/workflows/build/badge.svg
    :alt: GitHub
.. |Coveralls| image:: https://coveralls.io/repos/github/vint21h/django-read-only-admin/badge.svg?branch=master
    :alt: Coveralls
.. |pypi-license| image:: https://img.shields.io/pypi/l/django-read-only-admin
    :alt: License
.. |pypi-version| image:: https://img.shields.io/pypi/v/django-read-only-admin
    :alt: Version
.. |pypi-django-version| image:: https://img.shields.io/pypi/djversions/django-read-only-admin
    :alt: Supported Django version
.. |pypi-python-version| image:: https://img.shields.io/pypi/pyversions/django-read-only-admin
    :alt: Supported Python version
.. |pypi-format| image:: https://img.shields.io/pypi/format/django-read-only-admin
    :alt: Package format
.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/django-read-only-admin
    :alt: Python wheel support
.. |pypi-status| image:: https://img.shields.io/pypi/status/django-read-only-admin
    :alt: Package status
.. _GitHub: https://github.com/vint21h/django-read-only-admin/actions/
.. _Coveralls: https://coveralls.io/github/vint21h/django-read-only-admin?branch=master
.. _pypi-license: https://pypi.org/project/django-read-only-admin/
.. _pypi-version: https://pypi.org/project/django-read-only-admin/
.. _pypi-django-version: https://pypi.org/project/django-read-only-admin/
.. _pypi-python-version: https://pypi.org/project/django-read-only-admin/
.. _pypi-format: https://pypi.org/project/django-read-only-admin/
.. _pypi-wheel: https://pypi.org/project/django-read-only-admin/
.. _pypi-status: https://pypi.org/project/django-read-only-admin/
