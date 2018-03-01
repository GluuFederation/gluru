# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0023_auto_20160101_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='is_alerts',
            field=models.BooleanField(default=True, verbose_name='Send alerts?'),
        ),
    ]
