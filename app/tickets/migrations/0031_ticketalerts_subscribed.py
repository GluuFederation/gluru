# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0030_auto_20160218_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketalerts',
            name='subscribed',
            field=models.BooleanField(default=False, help_text='User is subscribed?', verbose_name='Subscribed?'),
        ),
    ]
