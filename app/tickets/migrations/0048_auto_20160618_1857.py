# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-18 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0047_auto_20160618_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.TextField(verbose_name='Answer'),
        ),
    ]