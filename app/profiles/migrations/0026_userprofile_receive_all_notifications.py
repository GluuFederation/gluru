# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-08 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0025_auto_20160916_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='receive_all_notifications',
            field=models.BooleanField(default=False),
        ),
    ]
