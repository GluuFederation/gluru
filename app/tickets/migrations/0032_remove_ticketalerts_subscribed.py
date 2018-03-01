# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0031_ticketalerts_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketalerts',
            name='subscribed',
        ),
    ]
