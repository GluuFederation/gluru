# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0019_auto_20151116_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='crm_id',
            field=models.CharField(max_length=36, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='crm_id',
            field=models.CharField(max_length=36, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ticketdocuments',
            name='crm_id',
            field=models.CharField(max_length=36, null=True, blank=True),
        ),
    ]
