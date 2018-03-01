# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20150902_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='ticket',
            field=models.ForeignKey(related_name='ticket_answers', verbose_name='Ticket', to='tickets.Ticket', help_text='Ticket'),
        ),
    ]
