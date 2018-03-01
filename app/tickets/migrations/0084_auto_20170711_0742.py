# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-11 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0083_ticket_gluu_server_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='os_version',
            field=models.CharField(blank=True, choices=[(b'', b'Select Operating System'), (b'U1404', b'Ubuntu 14.04'), (b'CentOS65', b'CentOS 6.5'), (b'CentOS66', b'CentOS 6.6'), (b'CentOS67', b'CentOS 6.7'), (b'CentOS72', b'CentOS 7.2'), (b'Rhel65', b'RHEL 6.5'), (b'Rhel66', b'RHEL 6.6'), (b'Rhel67', b'RHEL 6.7'), (b'Rhel72', b'RHEL 7.2'), (b'Other', b'Other')], max_length=8, null=True, verbose_name='Which OS are you using?'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_category',
            field=models.CharField(choices=[(b'', b'Select an issue category'), (b'installation', b'Installation'), (b'outages', b'Outages'), (b'single_sign_on', b'Single Sign-On'), (b'authentication', b'Authentication'), (b'authorization', b'Authorization'), (b'access_management', b'Access Management'), (b'upgrade', b'Upgrade'), (b'maintenance', b'Maintenance'), (b'identity_management', b'Identity Management'), (b'customization', b'Customization'), (b'feature_request', b'Feature Request'), (b'other', b'Other')], max_length=20, verbose_name='Category'),
        ),
    ]
