# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-15 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0037_auto_20170915_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitlements',
            name='plan',
            field=models.CharField(default=2, max_length=100, verbose_name='plan'),
            preserve_default=False,
        ),
    ]