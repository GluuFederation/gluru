# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0016_auto_20151023_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketdocuments',
            name='ticket',
            field=models.ForeignKey(related_name='ticket_documents', blank=True, to='tickets.Ticket', null=True),
        ),
    ]
