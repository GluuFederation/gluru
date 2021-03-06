# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0044_auto_20160524_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='gluu_server_version_comments',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Gluu Server Version'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='slug',
            field=models.CharField(db_index=True, help_text='Slug', max_length=255, verbose_name='Slug'),
        ),
    ]
