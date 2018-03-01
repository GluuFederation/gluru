# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0028_remove_ticket_modified_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='crm_id',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='crm_id',
        ),
    ]
