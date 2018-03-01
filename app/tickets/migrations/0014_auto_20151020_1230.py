# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0013_auto_20151019_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='description',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='title',
        ),
        migrations.AddField(
            model_name='answer',
            name='answer',
            field=models.TextField(default=b'', verbose_name='Answer'),
        ),
        migrations.AddField(
            model_name='answer',
            name='send_copy',
            field=models.CharField(default=b'', max_length=255, verbose_name='Send copy to', blank=True),
        ),
    ]
