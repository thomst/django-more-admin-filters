# -*- coding: utf-8 -*-

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from ...models import ModelA, ModelB


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

    for i in range(1, 30):
        model_a = ModelA()
        model_b = ModelB()

        model_b.id = i
        model_b.save()

        model_a.dropdown_less_than_four = i % 3
        model_a.dropdown_more_than_three = i % 4
        model_a.choices_dropdown = i % 9 +1
        model_a.multiselect = i % 4
        model_a.multiselect_dropdown = i % 4
        model_a.related_dropdown = model_b
        model_a.multiselect_related = model_b
        model_a.multiselect_related_dropdown = model_b
        model_a.save()


class Command(BaseCommand):
    help = 'Create test data.'

    def handle(self, *args, **options):
        create_test_data()
        # if options['create_test_data']:
