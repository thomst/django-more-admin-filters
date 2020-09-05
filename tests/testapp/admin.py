# -*- coding: utf-8 -*-

from django.contrib import admin
from more_admin_filters import (
    MultiSelectFilter, MultiSelectRelatedFilter, MultiSelectDropdownFilter,
    MultiSelectRelatedDropdownFilter, DropdownFilter, ChoicesDropdownFilter,
    RelatedDropdownFilter, BooleanAnnotationFilter
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
        'annotation_view',
        'boolean_annotation_view',
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
        BooleanAnnotationFilter.init('boolean_annotation'),
    )

    def annotation_view(self, obj):
        return obj.annotation

    def boolean_annotation_view(self, obj):
        return obj.boolean_annotation