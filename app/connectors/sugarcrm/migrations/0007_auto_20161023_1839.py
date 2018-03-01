# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-23 18:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sugarcrm', '0006_auto_20160709_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crmaccount',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sugar_crm', to=settings.AUTH_USER_MODEL),
        ),
    ]
