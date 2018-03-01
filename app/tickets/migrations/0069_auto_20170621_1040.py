# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0068_ticketnotification_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='os_version',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Which OS are you using?', choices=[(b'', b'Select Operating System'), (b'Ubuntu', b'Ubuntu'), (b'CentOS', b'CentOS'), (b'Rhel', b'Rhel'), (b'Debian', b'Debian')]),
        ),
    ]
