# Welcome to django-more-admin-filters

[![Run tests for django-more-admin-filters](https://github.com/thomst/django-more-admin-filters/actions/workflows/ci.yml/badge.svg)](https://github.com/thomst/django-more-admin-filters/actions/workflows/ci.yml)
[![coveralls badge](https://coveralls.io/repos/github/thomst/django-more-admin-filters/badge.svg?branch=master)](https://coveralls.io/github/thomst/django-more-admin-filters?branch=master)
[![python: 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3,13](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
[![django: 2.2, 3.0, 3.1, 3.2, 4.0, 4.1, 4.2, 5.0, 5.1, 5.2, 6.0](https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange)](https://img.shields.io/badge/django-2.2%20%7C%203.0%20%7C%203.1%20%7C%203.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange)

> **Note**
> If you are looking for a generic way of building and applying complex filters with a dynamic form right in the django admin backend, please checkout [django-searchkit](https://github.com/thomst/django-searchkit).

## Description

**Django-more-admin-filters** is a collection of Django admin filters with a focus on filters using dropdown widgets, multiple choice filters and filters working with annotated attributes.

## Installation

Install from pypi.org:

```bash
pip install django-more-admin-filters
```

Add `more_admin_filters` to your installed apps:

```python
INSTALLED_APPS = [
    'more_admin_filters',
    ...
]
```

Use the filter classes with your `ModelAdmin`:

```python
from more_admin_filters import MultiSelectDropdownFilter

class MyModelAdmin(admin.ModelAdmin):
    ...
    list_filter = [
        ('myfield', MultiSelectDropdownFilter),
        ...
    ]
```

Since the `ModelAdmin` routine to initialize the list filters doesn't work with annotated attributes, the usage for an annotation filter is a little bit special. The filter class needs to be equipped with the attribute's name:

```python
MyModelAdmin(admin.ModelAdmin):
    list_filter = [
        BooleanAnnotationFilter.init('my_annotated_attribute'),
        ...
    ]
```

## Filter classes

- **DropdownFilter**
  Dropdown filter for all kinds of fields.
- **ChoicesDropdownFilter**
  Dropdown filter for fields using choices.
- **RelatedDropdownFilter**
  Dropdown filter for relation fields.
- **RelatedOnlyDropdownFilter**
  Dropdown filter for relation fields using `limit_choices_to`.
- **MultiSelectFilter**
  Multi select filter for all kinds of fields.
- **MultiSelectRelatedFilter**
  Multi select filter for relation fields.
- **MultiSelectRelatedOnlyFilter**
  Multi select filter for related fields with choices limited to the objects involved in that relation.
- **MultiSelectDropdownFilter**
  Multi select dropdown filter for all kinds of fields.
- **MultiSelectRelatedDropdownFilter**
  Multi select dropdown filter for relation fields.
- **MultiSelectRelatedOnlyDropdownFilter**
  Multi select dropdown filter for relation fields with choices limited to the objects involved in that relation.
- **BooleanAnnotationFilter**
  Filter for annotated boolean attributes.

> **Note**
> More kinds of annotation filters will be added in future versions.
