# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0004_auto_20160307_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsent',
            name='alert_type',
            field=models.CharField(default='', max_length=100, verbose_name='Type'),
            preserve_default=False,
        ),
    ]
