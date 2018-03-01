# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0018_auto_20151023_1339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketdocuments',
            old_name='user',
            new_name='created_by',
        ),
        migrations.AddField(
            model_name='ticketdocuments',
            name='crm_id',
            field=uuidfield.fields.UUIDField(max_length=36, null=True, blank=True),
        ),
    ]
