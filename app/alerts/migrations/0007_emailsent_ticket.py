# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0037_auto_20160229_1919'),
        ('alerts', '0006_emailsent_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsent',
            name='ticket',
            field=models.ForeignKey(related_name='emails_sent', blank=True, to='tickets.Ticket', help_text='Ticket', null=True, verbose_name='Ticket'),
        ),
    ]
