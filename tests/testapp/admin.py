# -*- coding: utf-8 -*-

from django.contrib import admin
from more_filters import (
    MultiSelectFilter, MultiSelectRelatedFilter, MultiSelectDropdownFilter,
    MultiSelectRelatedDropdownFilter, DropdownFilter, ChoicesDropdownFilter,
    RelatedDropdownFilter, PlusMinusFilter, AnnotationListFilter,
    BooleanAnnotationListFilter
)
from .models import ModelA
from .models import ModelB


@admin.register(ModelA)
class ModelAAdmin(admin.ModelAdmin):
    search_fields = ('dropdown_less_than_four',)
    list_display = (
        'dropdown_less_than_four',
        'dropdown_more_than_three',
        'multiselect',
        'multiselect_dropdown',
        'choices_dropdown',
        'related_dropdown',
        'multiselect_related',
        'multiselect_related_dropdown',
    )

    list_filter = (
        ('dropdown_less_than_four', DropdownFilter),
        ('dropdown_more_than_three', DropdownFilter),
        ('multiselect', MultiSelectFilter),
        ('multiselect_dropdown', MultiSelectDropdownFilter),
        ('choices_dropdown', ChoicesDropdownFilter),
        ('related_dropdown', RelatedDropdownFilter),
        ('multiselect_related', MultiSelectRelatedFilter),
        ('multiselect_related_dropdown', MultiSelectRelatedDropdownFilter),
    )
