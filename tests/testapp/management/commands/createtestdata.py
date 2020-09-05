# -*- coding: utf-8 -*-

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from ...models import ModelA, ModelB, ModelC


def create_test_data():
    try:
        User.objects.create_superuser(
            'admin',
            'admin@testapp.org',
            'adminpassword')
    except IntegrityError:
        pass

    # clear existing data
    ModelA.objects.all().delete()
    ModelB.objects.all().delete()

    # TODO: create null values as well
    c_models = list()
    for i in range(36):

        if i > 0:
            model_a = ModelA()
            model_b = ModelB()
            model_c = ModelC()

            model_b.id = i
            model_b.save()
            model_c.id = i
            model_c.save()
            c_models.append(model_c)

            model_a.dropdown_lte3 = None if i % 3 == 0 else i % 3
            model_a.dropdown_gt3 = i % 4
            model_a.choices_dropdown = i % 9 +1
            model_a.multiselect = i % 5
            model_a.multiselect_dropdown = i % 6
            model_a.related_dropdown = model_b
            model_a.multiselect_related = model_b
            model_a.multiselect_related_dropdown = model_b
            model_a.save()
            model_a.c_models.set(c_models)
        else:
            model_a = ModelA()
            model_a.save()



class Command(BaseCommand):
    help = 'Create test data.'

    def handle(self, *args, **options):
        create_test_data()
        # if options['create_test_data']:
