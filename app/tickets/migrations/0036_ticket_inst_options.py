# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0035_ticketdocuments_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='inst_options',
            field=models.CharField(default=b'product', choices=[(1, b'What version OS are you using: Is it 64-bit hardware?'), (2, b'Does the Server have at least 4 GB RAM?')], max_length=255, blank=True, help_text='Please note that logs may                     also be needed. Please use an external service                     to link to those in your ticket.', verbose_name='Info'),
        ),
    ]
