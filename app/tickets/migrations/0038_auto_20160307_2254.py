# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0037_auto_20160229_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='inst_options',
            field=models.CharField(default=b'product', max_length=255, blank=True, help_text='Please note that logs may                     also be needed. Please use an external service                     to link to those in your ticket.', null=True, verbose_name='Info'),
        ),
    ]
