# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='activation_key',
            field=models.CharField(default='', max_length=40, verbose_name='activation key'),
            preserve_default=False,
        ),
    ]