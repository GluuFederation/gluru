# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0020_auto_20151116_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickethistory',
            name='after_value',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tickethistory',
            name='before_value',
            field=models.TextField(null=True, blank=True),
        ),
    ]
