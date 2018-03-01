# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-13 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0042_auto_20160504_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='date_start',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='etc',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='integration_type',
            field=models.CharField(blank=True, choices=[(b'', b'Select Integration Type'), (b'Mfa', b'Multi-Factor Authentication'), (b'Sso', b'Single Sign-On'), (b'Access', b'Access Management'), (b'Idnty', b'Identity Management'), (b'Other', b'Other')], max_length=8, null=True, verbose_name='Type of integration?'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='os_type',
            field=models.BooleanField(default=False, verbose_name='Is it 64-bit hardware?'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='os_version',
            field=models.CharField(blank=True, choices=[(b'', b'Select Operating System'), (b'U1404', b'Ubuntu 14.04'), (b'CentOS65', b'CentOS 6.5'), (b'CentOS66', b'CentOS 6.6'), (b'CentOS67', b'CentOS 6.7'), (b'CentOS72', b'CentOS 7.2'), (b'Rhel65', b'RHEL 6.5'), (b'Rhel66', b'RHEL 6.6'), (b'Rhel67', b'RHEL 6.7')], max_length=8, null=True, verbose_name='Which OS are you using?'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ram',
            field=models.BooleanField(default=False, verbose_name='Does the server have at least 4GB RAM?'),
        ),
    ]
