# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_auto_20150919_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='answers_no',
            field=models.IntegerField(default=0, help_text='Ticket answers number', verbose_name='Answers number', blank=True),
        ),
    ]
