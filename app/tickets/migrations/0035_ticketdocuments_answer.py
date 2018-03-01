# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0034_auto_20160226_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdocuments',
            name='answer',
            field=models.ForeignKey(related_name='answer_documents', blank=True, to='tickets.Answer', null=True),
        ),
    ]
