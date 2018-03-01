# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alert',
            options={'ordering': ('alert_order',), 'verbose_name': 'Alert', 'verbose_name_plural': 'Alerts'},
        ),
        migrations.AddField(
            model_name='alert',
            name='alert_option',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='alertoption',
            name='email_host',
            field=models.CharField(default=b'', help_text='Email host', max_length=100, verbose_name='Email host', blank=True),
        ),
        migrations.AlterField(
            model_name='alertoption',
            name='from_email',
            field=models.CharField(default=b'', help_text='From email', max_length=100, verbose_name='From email', blank=True),
        ),
        migrations.AlterField(
            model_name='alertoption',
            name='host_pass',
            field=models.CharField(default=b'', help_text='Host password', max_length=100, verbose_name='Host password', blank=True),
        ),
        migrations.AlterField(
            model_name='alertoption',
            name='host_user',
            field=models.CharField(default=b'', help_text='Email host user', max_length=100, verbose_name='Email host user', blank=True),
        ),
        migrations.AlterField(
            model_name='alertoption',
            name='port',
            field=models.CharField(default=b'', help_text='Port', max_length=100, verbose_name='Port', blank=True),
        ),
    ]
