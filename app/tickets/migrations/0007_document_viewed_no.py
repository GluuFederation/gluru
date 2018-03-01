# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_auto_20150916_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='viewed_no',
            field=models.IntegerField(default=0, help_text='Document number of views', verbose_name='Viewed', blank=True),
        ),
    ]
