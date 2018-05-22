#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-read-only-admin
# setup.py

from setuptools import (
    setup,
    find_packages,
)


# metadata
VERSION = (0, 1, 3)
__version__ = ".".join(map(str, VERSION))

setup(
    name="django-read-only-admin",
    version=__version__,
    packages=find_packages(),
    install_requires=["Django", ],
    author="Alexei Andrushievich",
    author_email="vint21h@vint21h.pp.ua",
    description="Really full django read only admin implementation",
    license="MIT",
    url="https://github.com/vint21h/django-read-only-admin/",
    download_url="https://github.com/vint21h/django-read-only-admin/archive/{version}.tar.gz".format(version=__version__),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Environment :: Plugins",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Framework :: Django :: 1.6",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
    ]
)
