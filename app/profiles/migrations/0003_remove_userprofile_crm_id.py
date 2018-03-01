# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150916_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='crm_id',
        ),
    ]
