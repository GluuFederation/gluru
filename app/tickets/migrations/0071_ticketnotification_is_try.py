# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-13 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0070_ticketnotification_is_call_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketnotification',
            name='is_try',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
