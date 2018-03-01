# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0067_remove_ticketnotification_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketnotification',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
