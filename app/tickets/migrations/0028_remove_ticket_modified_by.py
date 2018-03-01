# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0027_ticket_modified_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='modified_by',
        ),
    ]
