# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-13 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0045_auto_20160529_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='os_version',
            field=models.CharField(blank=True, choices=[(b'', b'Select Operating System'), (b'U1404', b'Ubuntu 14.04'), (b'CentOS65', b'CentOS 6.5'), (b'CentOS66', b'CentOS 6.6'), (b'CentOS67', b'CentOS 6.7'), (b'CentOS72', b'CentOS 7.2'), (b'Rhel65', b'RHEL 6.5'), (b'Rhel66', b'RHEL 6.6'), (b'Rhel67', b'RHEL 6.7'), (b'Rhel72', b'RHEL 7.2')], max_length=8, null=True, verbose_name='Which OS are you using?'),
        ),
    ]