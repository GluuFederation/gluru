# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-05 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0085_auto_20170905_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='os',
        ),
        migrations.AddField(
            model_name='ticket',
            name='os_version_name',
            field=models.FloatField(blank=True, null=True, verbose_name='OS Version'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='os_version',
            field=models.CharField(blank=True, choices=[(b'', b'Select Operating System'), (b'Ubuntu', b'Ubuntu'), (b'CentOS', b'CentOS'), (b'Rhel', b'RHEL'), (b'Debian', b'Debian')], max_length=8, null=True, verbose_name='Which OS are you using?'),
        ),
    ]
