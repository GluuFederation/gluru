# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-11-28 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0107_ticketdocuments_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdocuments',
            name='file_src',
            field=models.TextField(blank=True, verbose_name='File Source'),
        ),
    ]
