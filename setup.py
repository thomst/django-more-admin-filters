#!/usr/bin/env python

import os
from setuptools import setup
from setuptools import find_namespace_packages
from pathlib import Path


def version():
    """Get the local package version."""
    namespace = {}
    path = Path("more_admin_filters", "__version__.py")
    exec(path.read_text(), namespace)
    return namespace["__version__"]


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding="utf-8") as file:
        return file.read()


version = version()
if "dev" in version:
    dev_status = "Development Status :: 3 - Alpha"
elif "beta" in version:
    dev_status = "Development Status :: 4 - Beta"
else:
    dev_status = "Development Status :: 5 - Production/Stable"


setup(
    name="django-more-admin-filters",
    version=version,
    description="Additional filters for django-admin.",
    long_description=read("README.rst"),
    author="Thomas Leichtfuß",
    author_email="thomas.leichtfuss@posteo.de",
    url="https://github.com/thomst/django-more-admin-filters",
    license="BSD License",
    platforms=["OS Independent"],
    packages=find_namespace_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "Django>=2.2,<5.0",
    ],
    classifiers=[
        dev_status,
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    zip_safe=True,
)
