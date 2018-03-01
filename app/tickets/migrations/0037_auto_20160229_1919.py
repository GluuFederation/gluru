# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0036_ticket_inst_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='inst_options',
            field=models.CharField(default=b'product', help_text='Please note that logs may                     also be needed. Please use an external service                     to link to those in your ticket.', max_length=255, verbose_name='Info', blank=True),
        ),
    ]
