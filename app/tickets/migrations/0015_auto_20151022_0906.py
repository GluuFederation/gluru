# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0014_auto_20151020_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='link_url',
            field=models.CharField(default=b'', max_length=255, verbose_name='Link URL', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='privacy',
            field=models.CharField(default=b'inherit', max_length=255, verbose_name='Privacy', blank=True, choices=[(b'inherit', 'Inherit'), (b'public', 'Public'), (b'private', 'Private')]),
        ),
        migrations.AlterField(
            model_name='ticketalerts',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
