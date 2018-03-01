# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0033_ticket_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='modified_by',
            field=models.ForeignKey(related_name='ticket_modified_by', verbose_name='Modified by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
