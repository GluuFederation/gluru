# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-29 06:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0035_entitlements'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entitlements',
            options={'ordering': ['plan'], 'verbose_name_plural': 'entitlements'},
        ),
    ]
