# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-12-08 13:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0111_auto_20171208_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='set_default_gluu',
        ),
    ]
