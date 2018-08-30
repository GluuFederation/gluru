# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_userprofile_crm_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='ip',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='company_admin',
            field=models.BooleanField(default=False),
        ),
    ]