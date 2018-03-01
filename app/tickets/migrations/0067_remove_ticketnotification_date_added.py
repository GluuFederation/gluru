# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0066_auto_20170501_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketnotification',
            name='date_added',
        ),
    ]
