# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_ticket_answers_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='date_due',
            new_name='due_date',
        ),
        migrations.AddField(
            model_name='ticket',
            name='send_copy',
            field=models.CharField(default=b'', help_text='Copy addr', max_length=255, verbose_name='Copy addr', blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(default=b'', help_text='This field supports markdown language.             <a target="_blank" href="http://dillinger.io/">Information here</a>', verbose_name='Description'),
        ),
    ]
