# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Count, Case, When, Value


class ModelAManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(annotation=Count('c_models'))
        qs = qs.annotate(boolean_annotation=Case(
            When(annotation__gt=12, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField()
            ))
        return qs


class ModelA(models.Model):
    objects = ModelAManager()
    CHOICES = (
        ('1', 'one'),
        ('2', 'two'),
        ('3', 'three'),
        ('4', 'four'),
        ('5', 'five'),
        ('6', 'six'),
        ('7', 'seven'),
        ('8', 'eight'),
        ('9', 'nine'),
    )
    dropdown_less_than_four = models.IntegerField()
    dropdown_more_than_three = models.IntegerField()
    multiselect = models.IntegerField()
    multiselect_dropdown = models.IntegerField()
    choices_dropdown = models.CharField(max_length=255, blank=True, choices=CHOICES)
    related_dropdown = models.ForeignKey('ModelB', on_delete=models.CASCADE, related_name='related_dropdown_reverse')
    multiselect_related = models.ForeignKey('ModelB', on_delete=models.CASCADE, related_name='multiselect_related_reverse')
    multiselect_related_dropdown = models.ForeignKey('ModelB', on_delete=models.CASCADE, related_name='multiselect_related_dropdown_reverse')
    c_models = models.ManyToManyField('ModelC')


class ModelB(models.Model):
    id = models.AutoField(primary_key=True)


class ModelC(models.Model):
    id = models.AutoField(primary_key=True)
