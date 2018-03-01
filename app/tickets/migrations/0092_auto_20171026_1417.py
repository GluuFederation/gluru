# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-10-26 14:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0091_auto_20171026_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketproduct',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_id', to='tickets.Ticket'),
        ),
    ]
