# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0005_emailsent_alert_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsent',
            name='subject',
            field=models.CharField(default='', max_length=250, verbose_name='Subject'),
            preserve_default=False,
        ),
    ]
