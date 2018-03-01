# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0075_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='product',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_category',
            field=models.CharField(max_length=20, verbose_name='Category'),
        ),
    ]
