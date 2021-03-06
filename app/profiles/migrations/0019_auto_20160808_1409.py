# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-08 14:09
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


def create_company_entries(apps, schema_editor):

    Company = apps.get_model('profiles', 'Company')
    Profile = apps.get_model('profiles', 'UserProfile')

    for user in Profile.objects.all():

        if user.crm_type == 'user':
            continue

        try:
            company = Company.objects.get(name=user.company)

        except ObjectDoesNotExist:

            company = Company(name=user.company)
            company.save()

        user.company_association = company
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0018_auto_20160808_1404'),
    ]

    operations = [migrations.RunPython(create_company_entries), ]
