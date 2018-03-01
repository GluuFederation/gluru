# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-23 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0080_auto_20170623_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='issue_type',
            field=models.CharField(blank=True, choices=[(b'', 'Please specify the kind of issue you have encountered'), (b'outage', 'Production Outage'), (b'impaired', 'Production Impaired'), (b'pre_production', 'Pre-Production Issue'), (b'minor', 'Minor Issue'), (b'new_development', 'New Development Issue')], default=b'', max_length=20, verbose_name='Issue type'),
        ),
    ]
