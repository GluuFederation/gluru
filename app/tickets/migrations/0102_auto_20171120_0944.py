# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-11-20 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import tickets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0101_auto_20171108_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketdocuments',
            name='file',
            field=models.FileField(blank=True, upload_to=tickets.models.ticket_file_path),
        ),
    ]
