# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0025_auto_20160106_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='slug',
            field=models.SlugField(default='', help_text='Slug', max_length=255, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default=b'low', max_length=100, verbose_name='Priority', choices=[(b'low', 'Low'), (b'medium', 'Medium'), (b'community', 'Community'), (b'high', 'High')]),
        ),
    ]
