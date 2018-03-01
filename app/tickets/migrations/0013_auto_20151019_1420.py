# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0012_auto_20151019_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tickethistory',
            old_name='after_value_text',
            new_name='after_value',
        ),
        migrations.RenameField(
            model_name='tickethistory',
            old_name='before_value_text',
            new_name='before_value',
        ),
        migrations.RemoveField(
            model_name='tickethistory',
            name='after_value_string',
        ),
        migrations.RemoveField(
            model_name='tickethistory',
            name='before_value_string',
        ),
        migrations.RemoveField(
            model_name='tickethistory',
            name='crm_id',
        ),
        migrations.RemoveField(
            model_name='tickethistory',
            name='data_type',
        ),
        migrations.AlterField(
            model_name='tickethistory',
            name='created_by',
            field=models.ForeignKey(related_name='ticket_history_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
