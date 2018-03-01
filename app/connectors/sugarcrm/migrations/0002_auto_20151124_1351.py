# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sugarcrm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sugarcrmconnectors',
            name='profile',
            field=models.ForeignKey(related_name='profile_sugarcrm_id', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
