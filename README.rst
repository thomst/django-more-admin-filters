====================================
Welcome to django-more-admin-filters
====================================

.. image:: https://github.com/thomst/django-more-admin-filters/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/thomst/django-more-admin-filters/actions/workflows/ci.yml
    :alt: Run tests for django-more-admin-filters

.. image:: https://coveralls.io/repos/github/thomst/django-more-admin-filters/badge.svg?branch=master
    :target: https://coveralls.io/github/thomst/django-more-admin-filters?branch=master
    :alt: coveralls badge

.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue
   :target: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue
   :alt: python: 3.6, 3.7, 3.8, 3.9, 3.10

.. image:: https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2-orange
   :target: https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2-orange
   :alt: django: 2.2, 3.0, 3.1, 3.2, 4.0, 4.1, 4.2


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
            ...
        ]

Since the ModelAdmin routine to initialize the list filters doesn't work with
annotated attributes the usage for an annotation filter is a little bit special.
The filter class needs to be equipped with the attribute's name::

    MyModelAdmin(admin.ModelAdmin):
    list_filter = [
        BooleanAnnotationFilter.init('my_annotated_attribute'),
        ...
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
* **MultiSelectRelatedOnlyFilter**
    Multi select filter for related fields with choices limited to the objects
    involved in that relation
* **MultiSelectDropdownFilter**
    Multi select dropdown filter for all kind of fields.
* **MultiSelectRelatedDropdownFilter**
    Multi select dropdown filter for relation fields.
* **BooleanAnnotationFilter**
    Filter for annotated boolean-attributes.


.. note:: More kind of annotation filters will be added in future versions.
