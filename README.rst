=====================================
Welcome to django-admin--more-filters
=====================================

.. image:: https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue
   :target: https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue
   :alt: python: 3.4, 3.5, 3.6, 3.7, 3.8

.. image:: https://img.shields.io/badge/django-1.11%20%7C%202.0%20%7C%202.1%20%7C%202.2%20%7C%203.0-orange
   :target: https://img.shields.io/badge/django-1.11%20%7C%202.0%20%7C%202.1%20%7C%202.2%20%7C%203.0-orange
   :alt: django: 1.11, 2.0, 2.1, 2.2, 3.0


Description
===========
Django-admin-more-filters is a collection of django admin filters with a focus
on filters allowing multiple choices and the support of dropdown widgets.


Installation
============
Install from pypi.org::

    pip install django-admin-more-filters

Add more_filters to your installed apps::

    INSTALLED_APPS = [
        'more_filters',
        ...
    ]

Use the filter classes with your ModelAdmin::

    from more_filters import MultiSelectDropdownFilter

    class MyModelAdmin(admin.ModelAdmin):
        ...
        list_filter = [
            ('myfield', MultiSelectDropdownFilter),
        ]


Filter classes
==============
TODO
