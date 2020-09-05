====================================
Welcome to django-more-admin-filters
====================================

.. image:: https://travis-ci.com/thomst/django-more-admin-filters.svg?branch=master
    :target: https://travis-ci.com/thomst/django-more-admin-filters
    
.. image:: https://coveralls.io/repos/github/thomst/django-more-admin-filters/badge.svg?branch=master
    :target: https://coveralls.io/github/thomst/django-more-admin-filters?branch=master

.. image:: https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue
   :target: https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue
   :alt: python: 3.4, 3.5, 3.6, 3.7, 3.8

.. image:: https://img.shields.io/badge/django-1.11%20%7C%202.0%20%7C%202.1%20%7C%202.2%20%7C%203.0-orange
   :target: https://img.shields.io/badge/django-1.11%20%7C%202.0%20%7C%202.1%20%7C%202.2%20%7C%203.0-orange
   :alt: django: 1.11, 2.0, 2.1, 2.2, 3.0


Description
===========
Django-more-admin-filters is a collection of django admin filters with a focus
on filters using dropdown widgets, multiple choice filters and filters working
with annotated attributes.


Installation
============
Install from pypi.org::

    pip install django-more-admin-filters

Add more_admin_filters to your installed apps::

    INSTALLED_APPS = [
        'more_admin_filters',
        ...
    ]

Use the filter classes with your ModelAdmin::

    from more_admin_filters import MultiSelectDropdownFilter

    class MyModelAdmin(admin.ModelAdmin):
        ...
        list_filter = [
            ('myfield', MultiSelectDropdownFilter),
        ]


Filter classes
==============

* **DropdownFilter**
    Dropdown filter for all kind of fields.
* **ChoicesDropdownFilter**
    Dropdown filter for fields using choices.
* **RelatedDropdownFilter**
    Dropdown filter for relation fields.
* **RelatedOnlyDropdownFilter**
    Dropdown filter for relation fields using limit_choices_to.
* **MultiSelectFilter**
    Multi select filter for all kind of fields.
* **MultiSelectRelatedFilter**
    Multi select filter for relation fields.
* **MultiSelectDropdownFilter**
    Multi select dropdown filter for all kind of fields.
* **MultiSelectRelatedDropdownFilter**
    Multi select dropdown filter for relation fields.
* **BooleanAnnotationFilter**
    Filter for annotated boolean-attributes.


.. note:: More kind of annotation filters will be added in future versions.
