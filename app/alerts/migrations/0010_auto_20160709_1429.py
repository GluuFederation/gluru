# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-09 14:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0009_auto_20160619_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailsent',
            name='ticket',
        ),
        migrations.DeleteModel(
            name='EmailSent',
        ),
    ]